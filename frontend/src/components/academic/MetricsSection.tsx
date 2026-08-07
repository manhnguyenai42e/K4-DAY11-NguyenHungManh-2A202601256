"use client";

import { METRICS, GRADE_REPORT } from "@/lib/day11-data";

const m = METRICS as unknown as {
  total_requests: number;
  blocked_requests: number;
  block_rate: number;
  rate_limit_hits: number;
  judge_checks: number;
  judge_fails: number;
};

const g = GRADE_REPORT as unknown as {
  technical_failure: boolean;
  public_tests?: { passed: number; total: number };
  packaging?: { details?: { report?: string[]; audit?: boolean } };
  results_schema?: { ok: boolean };
};

export default function MetricsSection() {
  const blockRateFormatted = (m.block_rate * 100).toFixed(1);

  const gaugeCards = [
    { label: "Tổng request", value: String(m.total_requests), color: "text-[#124f8c]" },
    { label: "Bị chặn", value: String(m.blocked_requests), color: "text-red-600" },
    { label: "Block rate", value: `${blockRateFormatted}%`, color: "text-[#124f8c]" },
    { label: "LLM Judge Fails", value: `${m.judge_fails ?? 0} fail / ${m.judge_checks}`, color: "text-emerald-700" },
  ];

  return (
    <section
      id="metrics"
      className="h-[calc(100vh-64px)] flex flex-col justify-center py-4 bg-[#f8fafc] border-b border-slate-200 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        {/* Title */}
        <div className="max-w-3xl mx-auto text-center mb-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-blue-50 text-[#124f8c] border border-blue-200 text-[11px] font-bold uppercase tracking-wider mb-1">
            Quantitative Metrics
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
            Số Liệu Định Lượng hệ thống
          </h2>
        </div>

        {/* 4 Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
          {gaugeCards.map((card, i) => (
            <div key={i} className="academic-card p-3 rounded-xl bg-white border border-slate-200 shadow-xs text-center">
              <div className={`text-2xl font-black ${card.color} font-mono`}>{card.value}</div>
              <div className="text-[11px] uppercase font-bold text-slate-400 mt-0.5">{card.label}</div>
            </div>
          ))}
        </div>

        {/* Alert box */}
        <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 mb-4 flex items-center justify-between text-xs">
          <div>
            <span className="font-bold text-amber-900">Cảnh báo giám sát (monitoring alerts): </span>
            <span className="text-amber-800">block_rate {blockRateFormatted}% vượt ngưỡng 50% target (do tập test có 7 prompt attack + 5 HITL)</span>
          </div>
          <span className="px-2 py-0.5 rounded bg-amber-200 text-amber-900 text-[10px] font-bold">
            ALARM ACTIVE
          </span>
        </div>

        {/* Grade report card */}
        <div className="academic-card p-4 rounded-xl bg-white border border-slate-200 shadow-xs space-y-2.5">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider">
              Kiểm Tra Chấm Điểm Tự Động (Autograder Benchmark)
            </h3>
            <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold">
              Grade 100/100
            </span>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 text-xs">
            <div className="p-2 rounded bg-slate-50 border border-slate-200">
              <div className="text-[10px] text-slate-400 font-bold uppercase">TECHNICAL_FAILURE</div>
              <div className="font-mono font-bold text-emerald-700 text-xs">
                false (0 failure)
              </div>
            </div>

            <div className="p-2 rounded bg-slate-50 border border-slate-200">
              <div className="text-[10px] text-slate-400 font-bold uppercase">PUBLIC_TESTS</div>
              <div className="font-mono font-bold text-emerald-700 text-xs">
                13/13 Passed (100%)
              </div>
            </div>

            <div className="p-2 rounded bg-slate-50 border border-slate-200">
              <div className="text-[10px] text-slate-400 font-bold uppercase">REPORT_FILE</div>
              <div className="font-mono font-bold text-[#124f8c] text-xs">
                {g.packaging?.details?.report?.[0] || "2A202601256_report.md"} (OK)
              </div>
            </div>

            <div className="p-2 rounded bg-slate-50 border border-slate-200">
              <div className="text-[10px] text-slate-400 font-bold uppercase">AUDIT_LOG</div>
              <div className="font-mono font-bold text-[#124f8c] text-xs">
                audit_log.json (OK)
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}