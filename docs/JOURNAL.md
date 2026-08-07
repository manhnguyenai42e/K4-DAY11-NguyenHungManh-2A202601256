# Multi-Agent Handover Journal

> File lưu vết bàn giao công việc giữa các AI agents (Gemini CLI, Codex, Claude Code, Antigravity).

## [2026-08-07] - Antigravity (Gemini 3.6 Flash)

### Trạng thái công việc
- **Frontend Dashboard:** Đã hoàn thành 100% việc scaffold và sửa lỗi build cho Academic Dashboard (Next.js 15 + Tailwind CSS v4).
- **Build Status:** `npm run build` đã PASS thành công (4/4 static pages generated, 0 error, 0 warning).
- **Dev Server:** Chạy local bình thường tại `http://localhost:14000`.

### Các bước tiếp theo (nếu có):
- Đã hoàn tất các hạng mục UI theo yêu cầu của dự án.
- Tất cả dữ liệu từ `outputs/*.json` đã được load động vào `frontend/src/lib/day11-data.ts`.

## [2026-08-07] - Claude Code

### Bối cảnh
Ban tổ chức cập nhật lại đề bài (`assignment11.md`) và merge nhánh "upgrade controlled agent security lab" — cấu trúc contract khác đề cũ (`assignment11_defense_pipeline.md`). Đã merge `origin/main` vào nhánh làm bài, giữ nguyên toàn bộ code Phần A/B đã hoàn thành, đồng thời giữ `README.md` sát bản gốc của ban tổ chức nhất có thể (chỉ thêm mục "Thông tin sinh viên" theo yêu cầu bắt buộc của `SUBMISSION.md`).

### Hướng dẫn chạy phần mở rộng: Web Dashboard & HITL qua Telegram
Đây là lớp demo trực quan phụ, **không thuộc rubric chấm điểm chính thức** (chấm điểm dùng `python main.py --part N` theo `assignment11.md`).

```env
# .env — thêm nếu muốn chạy dashboard/Telegram HITL (không cần cho phần chấm điểm)
OPENAI_API_KEY=sk-proj-...
DEEPSEEK_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-v1-...
TELE_BOT_TOKEN=<telegram-bot-token-của-bạn>
TELE_BOT_ID=<telegram-chat-id-của-bạn>
HITL_ADMIN_TOKEN=<chuỗi-ngẫu-nhiên-tự-sinh>   # bắt buộc để /api/chat/action không bị mở công khai
```

```powershell
cd frontend && npm install && cd ..

# Terminal 1 — Backend FastAPI (poll Telegram HITL nền)
python -m uvicorn src.api_server:app --host 0.0.0.0 --port 14001

# Terminal 2 — Frontend Next.js
cd frontend && npm run dev
```

Truy cập `http://localhost:14000` (trang academic) hoặc `http://localhost:14000/chat` (chatbot UI + admin controls, cần `NEXT_PUBLIC_HITL_ADMIN_TOKEN` trong `frontend/.env.local` khớp `HITL_ADMIN_TOKEN` ở backend).

Deploy Vercel (tuỳ chọn): repo có `vercel.json` ở root trỏ build vào `frontend/`. Import repo, giữ Root Directory `./` (Vercel tự đọc `vercel.json`) hoặc chọn `frontend` theo khuyến nghị Vercel Monorepo.

### Vá bảo mật trong lớp mở rộng
- `src/api_server.py` `/api/chat/action` trước đây không xác thực — ai biết `ticket_id` cũng tự approve/reject được. Đã thêm header `X-Admin-Token` bắt buộc khớp `HITL_ADMIN_TOKEN`.
- `src/hitl/telegram_bot.py` sinh `ticket_id` từ `time.time() % 100000` — dễ đoán/liệt kê. Đã đổi sang `secrets.token_hex(4)`.
