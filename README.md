# Day 11 — Controlled Agent Security (2026)

Dự án nghiên cứu & triển khai hệ thống an toàn thông tin nhiều lớp cho AI Chatbot Ngân Hàng VinBank, mở rộng thêm **Web Dashboard (Next.js)** và **Human-in-the-Loop qua Telegram Bot** trên nền pipeline chuẩn của đề bài.

**Hình thức:** bài tập **cá nhân** (1 người / 1 MSSV).

**Đề bài duy nhất:** [`assignment11.md`](assignment11.md) · Cách nộp: [`SUBMISSION.md`](SUBMISSION.md)

---

## Thông tin sinh viên

| Thông tin | Giá trị |
|-----------|---------|
| Họ tên | Nguyễn Hùng Mạnh |
| MSSV | `2A202601256` |
| Framework | Google ADK (plugins) + pure-Python pipeline wrapper |
| Mô hình chính (pipeline chấm điểm) | Gemini (`GOOGLE_API_KEY`) |
| Mở rộng (dashboard/demo) | OpenAI `gpt-4o-mini` + fallback DeepSeek / OpenRouter |
| Web Frontend (mở rộng, tuỳ chọn) | `http://localhost:14000` |
| Backend API (mở rộng, tuỳ chọn) | `http://localhost:14001` |

---

## Cài đặt môi trường (làm trước)

```powershell
# 1) Tạo + kích hoạt virtualenv (khuyến nghị)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) API key
Copy-Item .env.example .env
# Mở .env, dán GOOGLE_API_KEY — lấy tại https://aistudio.google.com/apikey

# 3) Cài dependency trong venv
python -m pip install -U pip
pip install -r requirements.txt
```

Mỗi lần mở terminal mới: `.\.venv\Scripts\Activate.ps1` rồi mới chạy code.

Nếu PowerShell báo không cho chạy script:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

PowerShell (nếu chưa load `.env`):

```powershell
$env:GOOGLE_API_KEY="dán-key-của-bạn"
```

---

## Rubric (tóm tắt)

Chi tiết đầy đủ trong [`assignment11.md`](assignment11.md).

| Năng lực | Điểm | Bạn làm gì |
|---|---:|---|
| Direct + indirect guardrails | 35 | Xử lý jailbreak, email/RAG untrusted, Unicode và false positive |
| Permission + HITL | 35 | Egress allowlist, high-risk action, approval/reject/timeout/audit |
| Output + incident response | 20 | Redact PII/secret, monitoring, correlation trace |
| Red team | 10 | Attack taxonomy và report source-to-sink |
| Bonus | +10 | Verifier replay xác nhận Guards leak; không tin transcript tự khai |

**Gợi ý:** làm **Phòng thủ (A)** trước, **Tấn công (B)** sau.

**Hạn nộp:** Thứ sáu **7/8**, **23:59 giờ Việt Nam (ICT)**.

| Tài liệu | Dùng để |
|----------|---------|
| [`assignment11.md`](assignment11.md) | **Đề bài duy nhất** (rubric + cách chạy A/B) |
| [`SUBMISSION.md`](SUBMISSION.md) | Cách nộp, tên file, cấu trúc thư mục |

---

## Timeline buổi lab

Hình thức: **cá nhân** (1 người / 1 MSSV). Luồng: **Setup → A → Break → B → Break → Demo**.

| # | Phần | Nội dung | Thời lượng |
|---|------|----------|-----------:|
| 0 | **Setup** | Cài đặt môi trường (`pip`, `GOOGLE_API_KEY`, chạy local) | 30' |
| 1 | **A · Phòng thủ** | 2A Input · 2B Output · 2C NeMo · Part 3 Testing · Part 4 HITL | 120' |
| — | **Break** | Nghỉ giải lao | 10' |
| 2 | **B · Tấn công** | Tấn công **Unsafe** (điểm B) + **Guards** (điểm cộng nếu LEAKED) | 60' |
| — | **Break** | Nghỉ giải lao | 10' |
| 3 | **Demo** | Demo cá nhân · attack prompting (cuối buổi) | 45' |
| | **Tổng** | Nội dung lab (+ nghỉ) | **245'** |
| | | + Setup | **+30'** |

**Điểm cộng Demo (trên lớp):** lên demo **+1** (nếu defense chặn thành công ≥5 prompt thì **×2**) · tấn công thành công (LEAKED) **+2**.

Chi tiết mốc Part B (60'):

| Mốc | Việc làm |
|-----|----------|
| 0–25' | TODO 13 — viết ≥5 prompt tấn công nâng cao trong `src/attacks/attacks.py` |
| 25–45' | Chạy attack trên unsafe rồi guards; quan sát `LEAKED` / `no secret leak` |
| 45–60' | TODO 14 — AI red team ≥5 attack; lưu `outputs/attack_results.json` |

Slide đầy đủ + timer trên lớp: [`Slide_Lab_Day11.html`](Slide_Lab_Day11.html).

---

## Tình huống

Chatbot ngân hàng **VinBank**. Agent "unsafe" cố ý chứa mật khẩu / API key trong system prompt.

```
Câu hỏi người dùng
    → Rate Limiter
    → Lọc đầu vào (Input Guardrails)
    → LLM trả lời
    → Lọc đầu ra (Output Guardrails + Judge)
    → Audit / Monitoring
    → Phản hồi
```

---

## Làm bài trên máy

> Đã cài môi trường ở mục **Cài đặt môi trường** phía trên chưa? Nếu chưa thì làm trước.

### Phần A — Phòng thủ

**Thứ tự:** sửa TODO trong file → rồi mới chạy lệnh. Chi tiết: [`assignment11.md`](assignment11.md) §5.

| Làm trước | File |
|-----------|------|
| TODO **1–3** | `src/guardrails/input_guardrails.py` |
| TODO **4–6** | `src/guardrails/output_guardrails.py` |
| TODO **7** (tuỳ chọn) | `src/guardrails/nemo_guardrails.py` |
| TODO **8** (+ egress 8A) | `src/assignment/*.py` → rồi `python main.py --part 5` |
| TODO **9–10** | `src/testing/testing.py` |
| TODO **11–12** | `src/hitl/hitl.py` |
| TODO **13–14** (phần B) | `src/attacks/attacks.py` |

Sau khi đã code, kiểm:

```powershell
cd src
python main.py --part 2    # sau TODO 1–6 (+7 NeMo)
python main.py --part 3    # sau TODO 9–10
python main.py --part 4    # sau TODO 11–12
python main.py --part 5    # sau TODO 8 → outputs/results.json (+ audit/metrics)
```

```powershell
pytest tests/smoke -q
pytest tests/public -q
python scripts/grade.py --submission-dir . --out outputs/grade_report.json
```

Viết `report/<MSSV>_report.md`.

### Phần B — Red team và bonus

1. Viết ≥5 prompt vào `src/attacks/attacks.py`
2. Chạy (tấn công **unsafe** rồi **guards**):

```powershell
cd src
python main.py --part 1
```

3. Unsafe = attack target để phân tích. Guards (`src/agents/guards_agent.py`) = **bonus chỉ khi verifier replay xác nhận leak**.
4. Lưu `outputs/attack_results.json` làm evidence; không tự cấp runtime score hoặc bonus.

Colab / Jupyter (tuỳ chọn): `notebooks/lab11_guardrails_hitl.ipynb`. Local là đủ.

Nộp theo [`SUBMISSION.md`](SUBMISSION.md).

---

## Mở rộng: Web Dashboard & HITL qua Telegram (ngoài rubric bắt buộc)

Ngoài pipeline chuẩn theo `assignment11.md` (dùng để chấm điểm qua `python main.py --part N`), repo có thêm một lớp demo trực quan:

- Backend FastAPI (`src/api_server.py`, port `14001`) — expose pipeline + poll Telegram cho HITL 2 chiều
- Frontend Next.js (`frontend/`, port `14000`) — dashboard academic + chatbot UI trực tiếp
- HITL qua Telegram Bot (`src/hitl/telegram_bot.py`) — admin approve/reject ngay trên Telegram, đồng bộ 2 chiều với Web UI

```
Người dùng đặt câu hỏi
     │
     ├──► [Lớp 1] Rate Limiter
     ├──► [Lớp 2] Input Guardrail (Prompt Injection / DAN)
     ├──► [Lớp 3] Model Layer (Gemini, fallback OpenAI/DeepSeek/OpenRouter cho dashboard)
     ├──► [Lớp 4] Output Guardrail (Redact PII & Secret)
     └──► [Lớp 5] LLM-as-Judge & HITL Admin Telegram Approval
             ├── Sync 1: Telegram Bot Alert (Inline Approve/Reject/Reply)
             └── Sync 2: Web UI Admin Controls (Approve/Reject trên Web)
```

### Chạy demo mở rộng (tuỳ chọn, không bắt buộc cho chấm điểm)

Thêm các key sau vào `.env` nếu muốn chạy dashboard/Telegram HITL (không cần cho `python main.py --part N`):

```env
OPENAI_API_KEY=sk-proj-...
DEEPSEEK_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-v1-...
TELE_BOT_TOKEN=<telegram-bot-token-của-bạn>
TELE_BOT_ID=<telegram-chat-id-của-bạn>
```

> **Không commit token thật vào `.env`** — chỉ dùng file `.env` local (đã có trong `.gitignore`).

```powershell
# Cài dependency frontend
cd frontend
npm install
cd ..

# Terminal 1 — Backend FastAPI (poll Telegram HITL nền)
python -m uvicorn src.api_server:app --host 0.0.0.0 --port 14001

# Terminal 2 — Frontend Next.js
cd frontend
npm run dev
```

Truy cập `http://localhost:14000` (trang academic) hoặc `http://localhost:14000/chat` (chatbot UI + admin controls).

### Deploy Vercel (tuỳ chọn)

Repo có `vercel.json` ở root trỏ build vào `frontend/`. Import repo vào Vercel:
- **Cách 1:** giữ Root Directory `./` — Vercel tự đọc `vercel.json` và build Next.js từ `frontend/`.
- **Cách 2 (theo khuyến nghị Vercel Monorepo):** chọn Root Directory là `frontend`.

---

## Cấu trúc repo

```
├── assignment11.md                     ← Đề bài duy nhất
├── SUBMISSION.md                       ← Quy định nộp
├── data/pii_hallucination_samples.json ← PII + ground_truth đối chiếu hallucination
├── src/
│   ├── assignment/                     ← Hạng mục A (Phòng thủ)
│   ├── attacks/                        ← Hạng mục B (Tấn công)
│   ├── agents/security_boundary.py     ← Reference provenance / action boundary
│   ├── agents/guards_agent.py          ← Guards Agent (mục tiêu bonus)
│   ├── guardrails/ testing/ hitl/      ← Module hỗ trợ phòng thủ
│   ├── api_server.py                   ← (mở rộng) FastAPI backend cho dashboard
│   ├── hitl/telegram_bot.py            ← (mở rộng) Telegram Bot HITL dual-sync
│   └── main.py
├── frontend/                           ← (mở rộng) Next.js dashboard + chatbot UI
├── notebooks/lab11_guardrails_hitl.ipynb
├── schemas/results.schema.json
├── scripts/grade.py
├── tests/
├── vercel.json                         ← (mở rộng) cấu hình deploy Vercel
├── Slide_Lab_Day11.html
└── .env.example
```

---

## Tài liệu tham khảo

- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [Google ADK](https://google.github.io/adk-docs/)
- [AI Safety Fundamentals](https://aisafetyfundamentals.com/)
- PIArena (ACL 2026) — prompt-injection attack/defense benchmark được tham khảo để bổ sung pattern đo ASR, registry plug-and-play và tấn công tiến hoá (strategy_search) vào báo cáo. Repo: `https://github.com/sleeepeer/PIArena`.
