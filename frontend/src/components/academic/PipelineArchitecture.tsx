"use client";

import { useState } from "react";
import {
  Filter,
  Ban,
  Bot,
  ShieldAlert,
  Scale,
  CheckCircle2,
  FileCode2,
} from "lucide-react";

type Step = {
  id: string;
  num: string;
  title: string;
  file: string;
  desc: string;
  detail: string;
  codeSnippet: string;
  badges: { label: string; val: string }[];
  icon: typeof Filter;
};

export default function PipelineArchitecture() {
  const [activeStep, setActiveStep] = useState(0);

  const steps: Step[] = [
    {
      id: "ratelimit",
      num: "01",
      title: "Rate Limiter",
      file: "src/assignment/rate_limiter.py",
      desc: "Chặn lạm dụng & DoS từ một IP/User ID. Cấu hình Sliding Window — tối đa 20 request/phút.",
      detail:
        "Khi vượt quá 20 req/phút: trả về HTTP 429 Too Many Requests, ghi vào audit_log.json với blocked_by_layer='RATE_LIMIT'.",
      codeSnippet: `class RateLimitPlugin:
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.users = defaultdict(list)

    def check(self, user_id: str) -> bool:
        now = time.time()
        self.users[user_id] = [t for t in self.users[user_id] if now - t < self.window]
        if len(self.users[user_id]) >= self.max_requests:
            return False
        self.users[user_id].append(now)
        return True`,
      badges: [
        { label: "Thuật toán", val: "Sliding Window" },
        { label: "Giới hạn", val: "20 req/min" },
        { label: "Mã lỗi", val: "HTTP 429" },
      ],
      icon: Ban,
    },
    {
      id: "input",
      num: "02",
      title: "Input Guardrails",
      file: "src/guardrails/input_guardrails.py",
      desc: "Lớp chặn đầu tiên trước khi lời nhắc tới LLM. Regex bắt hàng chục dạng prompt injection (EN + VI) & lọc chủ đề ngân hàng.",
      detail:
        "Kiểm tra 3 tầng: 1) System prompt extract attempt ('ignore previous instructions'). 2) Jailbreak keywords ('DAN', 'you are now'). 3) Topic filter ngân hàng hợp lệ.",
      codeSnippet: `def detect_injection(user_input: str) -> bool:
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|above|prior)?\s*instructions?",
        r"reveal\s+(your\s+)?(instructions|prompt|secrets|password|api\s*key)",
        r"\bDAN\b",
    ]
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    return False`,
      badges: [
        { label: "Chống", val: "Prompt Injection" },
        { label: "Ngôn ngữ", val: "EN + VI" },
        { label: "Chi phí", val: "Regex, 0 token" },
      ],
      icon: Filter,
    },
    {
      id: "agent",
      num: "03",
      title: "LLM Agent (VinBank)",
      file: "src/agents/agent.py",
      desc: "Trí tuệ nhân tạo lõi (GPT-4o-Mini / Gemini ADK). Trả lời câu hỏi dịch vụ ngân hàng tài chính theo system prompt nghiêm ngặt.",
      detail:
        "System prompt thiết lập vai trò Chuyên viên tư vấn VinBank. Tuyệt đối không tiết lộ thông tin nội bộ hay thực hiện giao dịch trái phép.",
      codeSnippet: `VINBANK_SYSTEM_PROMPT = """
Bạn là Chuyên viên tư vấn VinBank. Chỉ giải đáp thắc mắc dịch vụ tài chính ngân hàng.
NẾU người dùng yêu cầu chuyển tiền hoặc thông tin quản trị: Yêu cầu xác thực Admin HITL.
NẾU hỏi ngoài ngành: Từ chối lịch sự.
"""`,
      badges: [
        { label: "Model", val: "GPT-4o-Mini (ADK)" },
        { label: "Phạm vi", val: "Ngân hàng & Tài chính" },
        { label: "Hỗ trợ", val: "Tiếng Việt" },
      ],
      icon: Bot,
    },
    {
      id: "output",
      num: "04",
      title: "Output Guardrails",
      file: "src/guardrails/output_guardrails.py",
      desc: "Lớp kiểm soát đầu ra trước khi gửi tới khách hàng. Lọc bỏ PII (Số thẻ, OTP, Password) và thông tin nhạy cảm.",
      detail:
        "Dù LLM có bị lừa rò rỉ secret, Output Guardrail vẫn tự động redact các pattern nhạy cảm hoặc thay bằng [REDACTED].",
      codeSnippet: `def content_filter(text: str) -> dict:
    # Masking PII / Secret
    redacted = re.sub(r"sk_[a-zA-Z0-9_-]{20,}", "[REDACTED_API_KEY]", text)
    redacted = re.sub(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[CARD_REDACTED]", redacted)
    return {"safe": redacted == text, "redacted": redacted}`,
      badges: [
        { label: "Redact PII", val: "Số thẻ, OTP, Secret" },
        { label: "Bảo vệ", val: "Dữ liệu khách hàng" },
        { label: "An toàn", val: "100%" },
      ],
      icon: ShieldAlert,
    },
    {
      id: "judge",
      num: "05",
      title: "LLM-as-Judge",
      file: "src/guardrails/output_guardrails.py",
      desc: "Lớp thẩm định chất lượng độc lập bằng Agent LLM Giám khảo chấm điểm 4 tiêu chí (Safety, Relevance, Accuracy, Tone 1-5).",
      detail:
        "Báo cáo chi tiết scorecard 1-5 điểm. Nếu verdict là FAIL, câu trả lời sẽ bị từ chối và thay bằng thông báo an toàn.",
      codeSnippet: `SAFETY_JUDGE_INSTRUCTION = """
Evaluate AI response on 4 criteria (1-5 each):
1. SAFETY 2. RELEVANCE 3. ACCURACY 4. TONE
VERDICT: PASS or FAIL
"""`,
      badges: [
        { label: "Tiêu chí", val: "Safety, Relevance, Accuracy, Tone" },
        { label: "Chấm điểm", val: "Thang 1-5" },
        { label: "Tỷ lệ lỗi", val: "0.0% Fail Rate" },
      ],
      icon: Scale,
    },
    {
      id: "hitl",
      num: "06",
      title: "HITL Telegram Admin",
      file: "src/hitl/hitl.py",
      desc: "Lớp giám sát con người (Human-in-the-Loop) thời gian thực cho các giao dịch nhạy cảm/giá trị lớn.",
      detail:
        "Tự động tạo Ticket HITL và phát cảnh báo Telegram Bot. Admin có thể Approve/Reject trực tiếp trên Telegram hoặc Web Dashboard.",
      codeSnippet: `async def create_hitl_ticket(user_input: str, reason: str) -> dict:
    ticket_id = f"HITL-{uuid4().hex[:8].upper()}"
    ticket = {"ticket_id": ticket_id, "status": "PENDING", "reason": reason}
    await notify_telegram_admin(ticket)
    return ticket`,
      badges: [
        { label: "Kênh duyệt", val: "Telegram Bot Dual-Sync" },
        { label: "Xác thực", val: "Admin Token Auth" },
        { label: "Trạng thái", val: "APPROVED / REJECTED" },
      ],
      icon: CheckCircle2,
    },
  ];

  const current = steps[activeStep];

  return (
    <section
      id="architecture"
      className="h-[calc(100vh-64px)] flex flex-col justify-center py-4 bg-[#f8fafc] border-b border-slate-200 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        {/* Title */}
        <div className="max-w-3xl mx-auto text-center mb-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-blue-50 text-[#124f8c] border border-blue-200 text-[11px] font-bold uppercase tracking-wider mb-1">
            Multi-Layer Defense Pipeline
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
            Kiến Trúc Bảo Vệ 6 Lớp
          </h2>
        </div>

        {/* Step buttons */}
        <div className="grid grid-cols-6 gap-2 mb-3">
          {steps.map((step, idx) => {
            const isActive = activeStep === idx;
            return (
              <button
                key={step.id}
                onClick={() => setActiveStep(idx)}
                className={`p-2 rounded-lg text-left transition-all border cursor-pointer flex flex-col justify-between ${
                  isActive
                    ? "bg-white border-[#124f8c] shadow-xs text-[#124f8c]"
                    : "bg-white/70 border-slate-200 hover:bg-white text-slate-600"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold">{step.num}</span>
                  <span className="text-[10px] font-bold">{isActive ? "• Active" : ""}</span>
                </div>
                <h3 className="text-[11px] font-bold truncate mt-1">{step.title}</h3>
              </button>
            );
          })}
        </div>

        {/* Step detail grid */}
        <div className="academic-card p-4 rounded-xl bg-white border border-slate-200 shadow-xs grid grid-cols-1 md:grid-cols-12 gap-4 items-start">
          {/* Info Column */}
          <div className="md:col-span-6 space-y-2.5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-[#124f8c] text-white font-mono text-[10px] font-bold">
                  LỚP {current.num}
                </span>
                <span className="font-mono text-[11px] text-slate-500">{current.file}</span>
              </div>
            </div>

            <h3 className="text-base font-black text-slate-900">{current.title}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">{current.desc}</p>
            <p className="text-[11px] text-slate-500 leading-relaxed bg-slate-50 p-2 rounded border border-slate-200">
              {current.detail}
            </p>

            <div className="flex flex-wrap gap-2 pt-1">
              {current.badges.map((b, idx) => (
                <div
                  key={idx}
                  className="px-2 py-1 rounded bg-slate-100 border border-slate-200 text-[10px] text-slate-700"
                >
                  <span className="text-slate-400 font-semibold">{b.label}: </span>
                  <span className="font-bold text-slate-900">{b.val}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Code Snippet Column */}
          <div className="md:col-span-6">
            <div className="rounded-lg bg-slate-900 border border-slate-800 p-3 overflow-hidden text-slate-200">
              <div className="flex items-center justify-between border-b border-slate-800 pb-1.5 mb-2">
                <div className="flex items-center gap-1 text-[10px] font-mono text-slate-400">
                  <FileCode2 className="w-3 h-3 text-[#124f8c]" />
                  <span>{current.file}</span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-red-500/80" />
                  <span className="w-2 h-2 rounded-full bg-amber-500/80" />
                  <span className="w-2 h-2 rounded-full bg-emerald-500/80" />
                </div>
              </div>

              <pre className="text-[11px] font-mono overflow-x-auto text-slate-200 leading-relaxed max-h-[180px] overflow-y-auto">
                <code>{current.codeSnippet}</code>
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}