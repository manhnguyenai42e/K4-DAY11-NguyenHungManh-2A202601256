"use client";

import {
  ShieldAlert,
  ShieldCheck,
  ArrowRight,
  Filter,
  Radio,
  Lock,
  Users,
} from "lucide-react";

export default function AcademicHero() {
  return (
    <section
      id="top"
      className="h-[calc(100vh-64px)] flex flex-col justify-center py-4 bg-gradient-to-b from-slate-50 via-white to-slate-50/50 border-b border-slate-200 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          {/* Left Column */}
          <div className="lg:col-span-7 space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-[#124f8c] text-[11px] font-bold uppercase tracking-wider">
              <span className="flex h-1.5 w-1.5 rounded-full bg-[#124f8c] animate-pulse" />
              Guardrails · HITL · Responsible AI (6 Lớp Defense-in-Depth)
            </div>

            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-black text-slate-900 tracking-tight leading-tight">
              Bảo Vệ Conversational AI Qua{" "}
              <span className="text-[#124f8c]">Trace 6 Lớp Guardrails</span> &amp; HITL
            </h1>

            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
              VinBank Assistant được trang bị <strong className="text-slate-900">6 lớp bảo vệ chuyên sâu</strong> — Rate Limiter, Input Guardrail, Gemini LLM Core, Output Guardrail (Redact PII/Secret), LLM-as-Judge 4 tiêu chí, và Telegram Admin Dual-Sync HITL. Đạt <strong className="text-emerald-700">100% tỷ lệ chặn tấn công &amp; 0% chặn nhầm safe query</strong>.
            </p>

            <div className="flex flex-wrap items-center gap-2.5 pt-1">
              <a
                href="/chat"
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-lg font-bold text-xs text-white bg-[#124f8c] hover:bg-[#0b355f] transition-all shadow-xs"
              >
                <span>Trải Nghiệm Live Chat (/chat)</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </a>
              <a
                href="#attacks"
                className="px-4 py-2.5 rounded-lg font-bold text-xs text-red-700 bg-red-50 border border-red-200 hover:bg-red-100 transition-all shadow-xs"
              >
                <span>Xem Ma Trận Attack</span>
              </a>
              <a
                href="#architecture"
                className="px-4 py-2.5 rounded-lg font-bold text-xs text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 transition-all shadow-xs"
              >
                <span>Kiến Trúc Pipeline 6 Lớp</span>
              </a>
            </div>

            {/* Badges */}
            <div className="pt-2 flex flex-wrap items-center gap-3 text-[11px] font-semibold text-slate-500">
              <div className="flex items-center gap-1">
                <Filter className="w-3 h-3 text-[#124f8c]" />
                <span>Google ADK · GPT-4o-Mini</span>
              </div>
              <div className="w-1 h-1 rounded-full bg-slate-300" />
              <div className="flex items-center gap-1">
                <Radio className="w-3 h-3 text-emerald-600" />
                <span>Pass 13/13 Tests</span>
              </div>
              <div className="w-1 h-1 rounded-full bg-slate-300" />
              <div className="flex items-center gap-1">
                <Users className="w-3 h-3 text-[#124f8c]" />
                <span>Telegram Bot Dual-Sync HITL</span>
              </div>
            </div>
          </div>

          {/* Right Preview Card */}
          <div className="lg:col-span-5">
            <div className="academic-card p-4 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider">
                  Kết Quả Trước &amp; Sau Guardrails
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  Passed 100%
                </span>
              </div>

              {/* Card 1 */}
              <div className="p-2.5 rounded-lg bg-red-50 border border-red-200 flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-slate-900">Unsafe Agent (Không Guardrails)</div>
                  <div className="text-[10px] text-slate-500">Secret admin &amp; API key trong prompt</div>
                </div>
                <div className="text-right">
                  <div className="text-red-700 font-bold text-xs">15/15 LEAKED</div>
                  <span className="text-[10px] text-red-600 font-mono">Rò rỉ 100%</span>
                </div>
              </div>

              {/* Card 2 */}
              <div className="p-2.5 rounded-lg bg-emerald-50/70 border border-emerald-200 flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-slate-900">Protected Agent (Guardrails)</div>
                  <div className="text-[10px] text-slate-500">Input gate + output filter hoạt động</div>
                </div>
                <div className="text-right">
                  <div className="text-emerald-700 font-bold text-xs">0/15 LEAKED</div>
                  <span className="text-[10px] text-emerald-600 font-mono">Chặn 100%</span>
                </div>
              </div>

              {/* Card 3 */}
              <div className="p-2.5 rounded-lg bg-blue-50/70 border border-blue-200 flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-slate-900">HITL Confidence Router</div>
                  <div className="text-[10px] text-slate-500">Auto-send / queue review / escalate</div>
                </div>
                <div className="text-right">
                  <div className="text-[#124f8c] font-bold text-xs">3 Decision Points</div>
                  <span className="text-[10px] text-blue-600 font-mono">confidence ≥ 0.9</span>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500 font-medium">Báo cáo kĩ thuật:</span>
                <a href="#report" className="font-bold text-[#124f8c] hover:underline">
                  Report 2A202601256 →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}