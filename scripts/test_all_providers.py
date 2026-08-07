"""
Test all 4 API providers from .env:
1. OpenRouter
2. Gemini
3. OpenAI
4. DeepSeek
"""
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)


def test_openrouter():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key or "your-" in key:
        return "SKIPPED", "No key configured"
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json"
    }
    body = {
        "model": os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash"),
        "messages": [{"role": "user", "content": "Say hello briefly"}],
        "max_tokens": 15
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return "PASSED", f"OK! Reply: '{content.strip()}'"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        return "FAILED", f"HTTP {e.code}: {err_body[:120]}"
    except Exception as e:
        return "FAILED", str(e)


def test_gemini():
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key or "your-" in key:
        return "SKIPPED", "No key configured"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key.strip()}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": "Say hello briefly"}]}]
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            return "PASSED", f"OK! Reply: '{content.strip()}'"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        return "FAILED", f"HTTP {e.code}: {err_body[:120]}"
    except Exception as e:
        return "FAILED", str(e)


def test_openai():
    key = os.getenv("OPENAI_API_KEY")
    if not key or "your-" in key:
        return "SKIPPED", "No key configured"
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Say hello briefly"}],
        "max_tokens": 15
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return "PASSED", f"OK! Reply: '{content.strip()}'"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        return "FAILED", f"HTTP {e.code}: {err_body[:120]}"
    except Exception as e:
        return "FAILED", str(e)


def test_deepseek():
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key or "your-" in key:
        return "SKIPPED", "No key configured"
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Say hello briefly"}],
        "max_tokens": 15
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return "PASSED", f"OK! Reply: '{content.strip()}'"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='ignore')
        return "FAILED", f"HTTP {e.code}: {err_body[:120]}"
    except Exception as e:
        return "FAILED", str(e)


if __name__ == "__main__":
    providers = [
        ("1. OpenRouter", test_openrouter),
        ("2. Gemini", test_gemini),
        ("3. OpenAI", test_openai),
        ("4. DeepSeek", test_deepseek),
    ]
    
    print("=" * 65)
    print(" TESTING API CALLS FOR ALL PROVIDERS IN .env ")
    print("=" * 65)
    
    for name, func in providers:
        status, details = func()
        print(f"[{status}] {name}: {details}")
    print("=" * 65)
