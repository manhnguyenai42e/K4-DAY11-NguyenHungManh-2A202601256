"""
HITL Telegram Bot Manager with Dual-Channel Web & Telegram Synchronization.
Sends notification alerts to Telegram Admin and listens for Inline Keyboard Callbacks / Direct Replies / Web UI Actions.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
TICKETS_FILE = OUTPUTS_DIR / "hitl_tickets.json"

load_dotenv(ROOT / ".env", override=True)

BOT_TOKEN = os.getenv("TELE_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELE_BOT_ID", "").strip()

_polling_task = None


def _load_tickets() -> Dict[str, Dict[str, Any]]:
    """Load tickets stored in outputs/hitl_tickets.json."""
    if not TICKETS_FILE.exists():
        return {}
    try:
        with open(TICKETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_tickets(tickets: Dict[str, Dict[str, Any]]):
    """Save tickets to outputs/hitl_tickets.json."""
    try:
        with open(TICKETS_FILE, "w", encoding="utf-8") as f:
            json.dump(tickets, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[HITL Telegram] Failed to save tickets file: {e}")


def create_hitl_ticket(prompt_text: str, user_id: str = "playground_user", reason: str = "Giao dịch giá trị lớn (> 50M VND)") -> str:
    """Tạo ticket HITL mới, lưu file và gửi Telegram Notification."""
    ticket_id = f"HITL-{int(time.time() * 1000) % 100000:04d}"
    
    tickets = _load_tickets()
    tickets[ticket_id] = {
        "ticket_id": ticket_id,
        "user_id": user_id,
        "prompt": prompt_text,
        "reason": reason,
        "status": "PENDING",  # PENDING, APPROVED, REJECTED, CUSTOM
        "response_text": None,
        "created_at": time.time(),
    }
    _save_tickets(tickets)
    
    # Send Telegram Notification
    send_hitl_telegram_notification(ticket_id, user_id, prompt_text, reason)
    return ticket_id


def get_hitl_ticket_status(ticket_id: str) -> Dict[str, Any] | None:
    """Lấy thông tin và trạng thái hiện tại của ticket từ file."""
    tickets = _load_tickets()
    return tickets.get(ticket_id)


def set_hitl_ticket_decision(ticket_id: str, action: str, custom_text: str | None = None) -> Dict[str, Any] | None:
    """Xử lý quyết định từ Web UI (Approve/Reject/Custom) và đồng bộ ngay sang Telegram."""
    tickets = _load_tickets()
    if ticket_id not in tickets:
        return None

    ticket = tickets[ticket_id]
    action_upper = action.upper()

    if action_upper == "APPROVED":
        ticket["status"] = "APPROVED"
        ticket["response_text"] = f"[APPROVED BY ADMIN (WEB UI)] Yêu cầu {ticket_id} đã được Admin phê duyệt thành công trên Web UI!"
        if BOT_TOKEN and CHAT_ID:
            _send_telegram_reply(int(CHAT_ID), f"✅ [WEB UI SYNC] Admin vừa CHẤP THUẬN Ticket {ticket_id} trên Web UI.")
    elif action_upper == "REJECTED":
        ticket["status"] = "REJECTED"
        ticket["response_text"] = f"[REJECTED BY ADMIN (WEB UI)] Yêu cầu {ticket_id} đã bị Admin từ chối trên Web UI."
        if BOT_TOKEN and CHAT_ID:
            _send_telegram_reply(int(CHAT_ID), f"❌ [WEB UI SYNC] Admin vừa TỪ CHỐI Ticket {ticket_id} trên Web UI.")
    elif action_upper == "CUSTOM" and custom_text:
        ticket["status"] = "CUSTOM"
        ticket["response_text"] = f"[ADMIN PHẢN HỒI (WEB UI)]: {custom_text}"
        if BOT_TOKEN and CHAT_ID:
            _send_telegram_reply(int(CHAT_ID), f"💬 [WEB UI SYNC] Admin vừa trả lời Ticket {ticket_id} trên Web UI: \"{custom_text}\"")

    _save_tickets(tickets)
    return ticket


def send_hitl_telegram_notification(ticket_id: str, user_id: str, prompt_text: str, reason: str) -> bool:
    """Gửi thông báo có Nút bấm Inline (Approve/Reject) đến Telegram Admin."""
    if not BOT_TOKEN or not CHAT_ID:
        print("[HITL Telegram] Missing TELE_BOT_TOKEN or TELE_BOT_ID in .env")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    msg_text = (
        f"🚨 <b>YÊU CẦU CẦN XÁC THỰC ADMIN (HITL ALERT)</b>\n\n"
        f"🆔 <b>Ticket ID:</b> <code>{ticket_id}</code>\n"
        f"👤 <b>Người dùng:</b> <code>{user_id}</code>\n"
        f"📝 <b>Nội dung yêu cầu:</b>\n<i>\"{prompt_text}\"</i>\n\n"
        f"⚠️ <b>Lý do cần duyệt:</b> {reason}\n\n"
        f"👉 <i>Bấm nút bên dưới để Duyệt/Từ chối hoặc trả lời trực tiếp tin nhắn này.</i>"
    )

    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ CHẤP THUẬN (APPROVE)", "callback_data": f"approve_{ticket_id}"},
                {"text": "❌ TỪ CHỐI (REJECT)", "callback_data": f"reject_{ticket_id}"},
            ]
        ]
    }

    payload = {
        "chat_id": CHAT_ID,
        "text": msg_text,
        "parse_mode": "HTML",
        "reply_markup": inline_keyboard,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                print(f"[HITL Telegram] Notification sent successfully for {ticket_id}!")
                return True
    except Exception as e:
        print(f"[HITL Telegram] Failed to send message: {e}")
    return False


async def poll_telegram_updates_loop():
    """Background polling loop lắng nghe Telegram Callback Query và Reply từ Admin."""
    if not BOT_TOKEN:
        return

    offset = 0
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    print("[HITL Telegram Poller] Background polling started...")

    while True:
        try:
            poll_url = f"{url}?offset={offset}&timeout=4"
            req = urllib.request.Request(poll_url)
            
            resp_data = await asyncio.to_thread(_fetch_json, req, 6)
            if resp_data and resp_data.get("ok"):
                for result in resp_data.get("result", []):
                    offset = max(offset, result["update_id"] + 1)
                    
                    # Handle Inline Button Click (callback_query)
                    if "callback_query" in result:
                        cb = result["callback_query"]
                        cb_id = cb["id"]
                        cb_data = cb.get("data", "")
                        
                        tickets = _load_tickets()
                        
                        if cb_data.startswith("approve_"):
                            tid = cb_data.replace("approve_", "")
                            if tid in tickets:
                                tickets[tid]["status"] = "APPROVED"
                                tickets[tid]["response_text"] = f"[APPROVED BY ADMIN] Yêu cầu {tid} đã được Admin phê duyệt thành công qua Telegram!"
                                _save_tickets(tickets)
                                print(f"[HITL Telegram Poller] APPROVED ticket {tid}")
                                await asyncio.to_thread(_answer_callback, cb_id, "CHAP THUAN YEU CAU THANH CONG!")
                                await asyncio.to_thread(_edit_telegram_message, cb["message"]["chat"]["id"], cb["message"]["message_id"], tid, "APPROVED")
                            else:
                                await asyncio.to_thread(_answer_callback, cb_id, f"Ticket {tid} expired or not found!")

                        elif cb_data.startswith("reject_"):
                            tid = cb_data.replace("reject_", "")
                            if tid in tickets:
                                tickets[tid]["status"] = "REJECTED"
                                tickets[tid]["response_text"] = f"[REJECTED BY ADMIN] Yêu cầu {tid} đã bị Admin từ chối do không đáp ứng tiêu chuẩn an toàn."
                                _save_tickets(tickets)
                                print(f"[HITL Telegram Poller] REJECTED ticket {tid}")
                                await asyncio.to_thread(_answer_callback, cb_id, "TU CHOI YEU CAU!")
                                await asyncio.to_thread(_edit_telegram_message, cb["message"]["chat"]["id"], cb["message"]["message_id"], tid, "REJECTED")
                            else:
                                await asyncio.to_thread(_answer_callback, cb_id, f"Ticket {tid} expired or not found!")

                    # Handle Direct Text Reply from Admin
                    elif "message" in result:
                        msg = result["message"]
                        text = msg.get("text", "")
                        
                        reply_to = msg.get("reply_to_message", {}).get("text", "")
                        tickets = _load_tickets()
                        for tid, ticket in tickets.items():
                            if (tid in text or tid in reply_to):
                                tickets[tid]["status"] = "CUSTOM"
                                tickets[tid]["response_text"] = f"[ADMIN PHẢN HỒI]: {text}"
                                _save_tickets(tickets)
                                print(f"[HITL Telegram Poller] CUSTOM REPLY for ticket {tid}: {text}")
                                await asyncio.to_thread(_send_telegram_reply, msg["chat"]["id"], f"💬 Đã gửi phản hồi trực tiếp cho {tid}: \"{text}\"")
                                break
        except Exception:
            pass
        
        await asyncio.sleep(1.5)


def _fetch_json(req: urllib.request.Request, timeout: int) -> dict | None:
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass
    return None


def _answer_callback(callback_query_id: str, text: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
        data = json.dumps({"callback_query_id": callback_query_id, "text": text, "show_alert": True}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=4)
    except Exception:
        pass


def _edit_telegram_message(chat_id: int, message_id: int, ticket_id: str, status: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
        icon = "✅" if status == "APPROVED" else "❌"
        label = "ĐÃ CHẤP THUẬN" if status == "APPROVED" else "ĐÃ TỪ CHỐI"
        text = f"{icon} <b>HITL TICKET {ticket_id}: {label} BY ADMIN</b>"
        data = json.dumps({"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=4)
    except Exception:
        pass


def _send_telegram_reply(chat_id: int, text: str):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=4)
    except Exception:
        pass


def start_telegram_poller_background():
    """Khởi động background polling task nếu chưa chạy."""
    global _polling_task
    try:
        loop = asyncio.get_running_loop()
        if _polling_task is None or _polling_task.done():
            _polling_task = loop.create_task(poll_telegram_updates_loop())
            print("[HITL Telegram] Polling task launched successfully!")
    except RuntimeError:
        pass
