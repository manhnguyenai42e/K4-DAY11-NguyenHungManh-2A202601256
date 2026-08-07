"""
Lightweight FastAPI server wrapping DefensePipeline and HITL Telegram Bot Manager.

Usage:
    python -m uvicorn src.api_server:app --host 0.0.0.0 --port 14001 --reload
"""
from __future__ import annotations

import os
import sys
import time
import re
from pathlib import Path

# Ensure src/ is on the path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load .env
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

HITL_ADMIN_TOKEN = os.getenv("HITL_ADMIN_TOKEN", "").strip()


def _require_admin(x_admin_token: str | None) -> None:
    """Chặn /api/chat/action nếu thiếu/sai admin token.

    Không có bước này, bất kỳ ai biết ticket_id đều tự approve/reject được
    yêu cầu HITL của chính mình — vô hiệu hoá toàn bộ mục đích human review.
    """
    if not HITL_ADMIN_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="HITL_ADMIN_TOKEN chưa được cấu hình trong .env — admin action bị khoá.",
        )
    if not x_admin_token or x_admin_token != HITL_ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Missing or invalid admin token")

from core.config import setup_api_key
from assignment.pipeline import DefensePipeline
from hitl.telegram_bot import (
    create_hitl_ticket,
    get_hitl_ticket_status,
    set_hitl_ticket_decision,
    start_telegram_poller_background,
)

# --- Setup ---
setup_api_key()
pipeline = DefensePipeline(max_requests=20, window_seconds=60, use_llm_judge=True)

app = FastAPI(title="VinBank Guardrails & HITL Chat API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:14000", "http://localhost:3000", "http://127.0.0.1:14000"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "playground_user"


class ChatResponse(BaseModel):
    input: str
    response: str
    blocked: bool
    layer: str | None
    latency_ms: float
    ticket_id: str | None = None
    status: str = "COMPLETED"


HITL_KEYWORDS = [
    r"100[\.,]?000[\.,]?000",
    r"50[\.,]?000[\.,]?000",
    r"100\s*triệu",
    r"50\s*triệu",
    r"rút\s*tiền\s*lớn",
    r"reset\s*password",
    r"đổi\s*mật\s*khẩu",
    r"nâng\s*hạn\s*mức",
    r"cấp\s*quyền",
    r"admin\s*duyệt",
    r"hitl",
]


def check_hitl_needed(text: str) -> bool:
    """Kiểm tra xem yêu cầu có thuộc danh mục cần Admin duyệt (HITL) hay không."""
    for pattern in HITL_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


@app.on_event("startup")
async def startup_event():
    """Khởi động Telegram Background Poller khi FastAPI server chạy."""
    start_telegram_poller_background()
    print("[API Server] HITL Telegram Background Poller Started!")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    t0 = time.perf_counter()

    # 1. Kiểm tra HITL (Human-in-the-Loop)
    if check_hitl_needed(req.message):
        ticket_id = create_hitl_ticket(
            prompt_text=req.message,
            user_id=req.user_id,
            reason="Yêu cầu giao dịch/thao tác nhạy cảm giá trị lớn cần Admin xác thực",
        )
        latency = (time.perf_counter() - t0) * 1000
        
        wait_text = (
            f"⏳ Xin bạn đợi mình một chút, yêu cầu của bạn thuộc danh mục giao dịch an toàn cao. "
            f"Hệ thống đã gửi thông báo đến Quản trị viên (Admin) qua Telegram để phê duyệt. "
            f"Mã vé xác thực: {ticket_id}."
        )

        return ChatResponse(
            input=req.message,
            response=wait_text,
            blocked=False,
            layer="HITL Telegram Guardrail (Lớp 5)",
            latency_ms=round(latency, 1),
            ticket_id=ticket_id,
            status="PENDING",
        )

    # 2. Xử lý qua 5 Lớp Pipeline thông thường
    try:
        result = await pipeline.process(req.message, user_id=req.user_id)
        latency = (time.perf_counter() - t0) * 1000

        return ChatResponse(
            input=result["input"],
            response=result.get("response_preview", ""),
            blocked=result["blocked"],
            layer=result.get("layer"),
            latency_ms=round(latency, 1),
            status="COMPLETED",
        )
    except Exception as e:
        latency = (time.perf_counter() - t0) * 1000
        err_msg = str(e)
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "Quota" in err_msg:
            resp_text = "⚠️ Gemini API (429 Resource Exhausted): Quota lượt gọi LLM hiện tại đã tạm hết lượt. Hệ thống vẫn bảo vệ an toàn các guardrails!"
            layer_name = "Gemini API Quota (429)"
        else:
            resp_text = f"⚠️ Lỗi xử lý backend: {err_msg[:180]}"
            layer_name = "Backend Error"

        return ChatResponse(
            input=req.message,
            response=resp_text,
            blocked=True,
            layer=layer_name,
            latency_ms=round(latency, 1),
            status="ERROR",
        )


class TicketActionRequest(BaseModel):
    ticket_id: str
    action: str  # APPROVED, REJECTED, CUSTOM
    response_text: str | None = None


@app.post("/api/chat/action")
async def process_ticket_action(
    req: TicketActionRequest, x_admin_token: str | None = Header(default=None)
):
    """Endpoint cho Web UI Admin thực hiện Approve / Reject / Custom reply và đồng bộ sang Telegram.

    Yêu cầu header ``X-Admin-Token`` khớp ``HITL_ADMIN_TOKEN`` trong .env —
    đây là hành động high-risk (tự phê duyệt giao dịch), không cho phép ẩn danh.
    """
    _require_admin(x_admin_token)
    ticket = set_hitl_ticket_decision(req.ticket_id, req.action, req.response_text)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "status": "success",
        "ticket_id": ticket["ticket_id"],
        "ticket_status": ticket["status"],
        "response_text": ticket.get("response_text"),
    }


@app.get("/api/chat/status/{ticket_id}")
async def check_ticket_status(ticket_id: str):
    """Endpoint cho Chat UI poll trạng thái ticket xem Admin đã duyệt chưa."""
    ticket = get_hitl_ticket_status(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "ticket_id": ticket["ticket_id"],
        "status": ticket["status"],
        "response_text": ticket.get("response_text"),
    }


@app.get("/api/health")
async def health():
    return {"status": "ok", "live": pipeline.live}
