"""
Lab 11 — Configuration & Multi-Provider API Key Setup.

Priority Order:
0. Local LLM (Unsloth/llama.cpp OpenAI-compatible server) — Primary Default
1. OpenAI (gpt-4o-mini)
2. DeepSeek (deepseek-v4-flash)
3. OpenRouter
4. Gemini
"""
from __future__ import annotations

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Load root .env
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")

# MSSV sinh viên
STUDENT_ID = "2A202601256"


def is_valid_key(key: str | None) -> bool:
    """Kiểm tra API Key có hợp lệ và không phải placeholder hay không."""
    if not key or not isinstance(key, str):
        return False
    k = key.strip()
    if not k or k.startswith("<") or k.endswith(">") or "your-" in k or k == "none":
        return False
    return True


def check_key_working(provider: str, key: str) -> bool:
    """Kiểm tra nhanh (ping 3s) xem API key có thực sự hoạt động."""
    try:
        if provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key.strip()}", "Content-Type": "application/json"}
            body = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1}
        elif provider == "deepseek":
            url = "https://api.deepseek.com/chat/completions"
            headers = {"Authorization": f"Bearer {key.strip()}", "Content-Type": "application/json"}
            body = {"model": "deepseek-chat", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1}
        elif provider == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key.strip()}", "Content-Type": "application/json"}
            body = {"model": "google/gemini-2.5-flash", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1}
        elif provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key.strip()}"
            headers = {"Content-Type": "application/json"}
            body = {"contents": [{"parts": [{"text": "hi"}]}]}
        elif provider == "local":
            base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:8888/v1").rstrip("/")
            url = f"{base_url}/models"
            headers = {"Authorization": f"Bearer {key.strip()}"} if key else {}
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status == 200
        else:
            return False

        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def setup_api_key() -> tuple[str, str]:
    """Cấu hình API Key với gpt-4o-mini làm mặc định chính:
    1. OpenAI (gpt-4o-mini) -> 2. DeepSeek -> 3. OpenRouter -> 4. Gemini
    Trả về (provider_name, model_name).
    """
    # Force reload .env
    load_dotenv(ROOT / ".env", override=True)

    # Priority 0: Local LLM (Unsloth / llama.cpp OpenAI-compatible server)
    local_base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:8888/v1")
    local_key = os.getenv("LOCAL_LLM_API_KEY", "")
    local_model_id = os.getenv("LOCAL_LLM_MODEL", "")
    if os.getenv("USE_LOCAL_LLM", "1") != "0" and local_model_id and check_key_working("local", local_key):
        os.environ["OPENAI_API_KEY"] = local_key.strip() or "local-no-auth"
        os.environ["OPENAI_BASE_URL"] = local_base_url
        model = f"openai:{local_model_id}"
        print(f"[API Provider - Primary] Selected Local LLM (Model: {model} @ {local_base_url})")
        return "local", model

    # Priority 1: OpenAI (gpt-4o-mini)
    openai_key = os.getenv("OPENAI_API_KEY")
    if is_valid_key(openai_key) and check_key_working("openai", openai_key):
        os.environ["OPENAI_API_KEY"] = openai_key.strip()
        if "OPENAI_BASE_URL" in os.environ:
            del os.environ["OPENAI_BASE_URL"]
        model = os.getenv("OPENAI_MODEL", "openai:gpt-4o-mini")
        if not model.startswith("openai:"):
            model = f"openai:{model}"
        print(f"[API Provider - Primary] Selected OpenAI (Model: {model})")
        return "openai", model

    # Priority 2: DeepSeek
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if is_valid_key(deepseek_key) and check_key_working("deepseek", deepseek_key):
        os.environ["OPENAI_API_KEY"] = deepseek_key.strip()
        os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"
        model = "openai:deepseek-chat"
        print(f"[API Provider - Fallback 2] Selected DeepSeek (Model: {model})")
        return "deepseek", model

    # Priority 3: OpenRouter
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if is_valid_key(openrouter_key) and check_key_working("openrouter", openrouter_key):
        os.environ["OPENAI_API_KEY"] = openrouter_key.strip()
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
        model = "openai:google/gemini-2.5-flash"
        print(f"[API Provider - Fallback 3] Selected OpenRouter (Model: {model})")
        return "openrouter", model

    # Priority 4: Gemini
    google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if is_valid_key(google_key) and check_key_working("gemini", google_key):
        os.environ["GOOGLE_API_KEY"] = google_key.strip()
        os.environ["GEMINI_API_KEY"] = google_key.strip()
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
        print(f"[API Provider - Fallback 4] Selected Google Gemini (Model: {model})")
        return "gemini", model

    # Fallback default
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
    print("[API Provider] Defaulting to gpt-4o-mini config.")
    return "openai", "openai:gpt-4o-mini"


def get_active_model() -> str:
    """Trả về tên model active phù hợp với provider đã được chọn."""
    _, model = setup_api_key()
    return model


# Allowed banking topics (used by topic_filter)
ALLOWED_TOPICS = [
    "banking", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit",
    "deposit", "withdrawal", "balance", "payment",
    "tai khoan", "tài khoản", "giao dich", "giao dịch", "tiet kiem", "tiết kiệm", "lai suat", "lãi suất",
    "chuyen tien", "chuyển tiền", "the tin dung", "thẻ tín dụng", "so du", "số dư", "vay",
    "ngan hang", "ngân hàng", "atm", "gui tien", "gửi tiền", "nap tien", "nạp tiền", "rut tien", "rút tiền",
    "xin chao", "xin chào", "chao", "chào", "hello", "hi", "tư vấn", "tu van", "trợ giúp", "tro giup",
]

# Blocked topics (immediate reject)
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal",
    "violence", "gambling", "bomb", "kill", "steal",
]
