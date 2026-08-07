"use client";

import { METRICS, GRADE_REPORT } from "@/lib/day11-data";

export default function ResearchAbstract() {
  const m = METRICS as unknown as { block_rate: number };
  const g = GRADE_REPORT as unknown as {
    technical_failure: boolean;
    public_tests: { returncode: number };
    packaging: { ok: boolean };
  };

  const blockRatePct = (m.block_rate * 100).toFixed(1);

  const facts = [
    { label: "grade_report · technical_failure", value: `${g.technical_failure} (0 failure)` },
    { label: "public_tests · returncode", value: `${g.public_tests?.returncode ?? 0} (PASSED)` },
    { label: "packaging · audit/metrics/results", value: `${g.packaging?.ok ? "ok (đầy đủ)" : "error"}` },
    { label: "alerts · block_rate", value: `${blockRatePct}% > 50% target` },
  ];

  return (
    <section id="abstract" className="h-[calc(100vh-64px)] flex flex-col justify-center py-4 bg-white border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="max-w-3xl mx-auto text-center mb-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-blue-50 text-[#124f8c] border border-blue-200 text-xs font-bold uppercase tracking-wider mb-2">
            Executive Summary
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Báo Cáo Lab Day 11 — Responsible AI
          </h2>
          <p className="text-slate-600 mt-2 text-xs sm:text-sm leading-relaxed">
            Mô tả ngắn: xây dựng hệ thống nhiều lớp bảo vệ cho assistant ngân hàng, chạy 15 attack
            vector, so sánh <strong>trước/sau</strong> guardrails, và thiết kế HITL để con người
            giám sát quyết định rủi ro cao.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-5xl mx-auto">
          {facts.map((f, i) => (
            <div key={i} className="bg-slate-50 border border-slate-200 p-4 rounded-xl text-center shadow-xs">
              <div className="text-[11px] uppercase font-bold text-slate-400 leading-tight mb-1">{f.label}</div>
              <div className="text-sm font-bold text-[#124f8c] font-mono">{f.value}</div>
            </div>
          ))}
        </div>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <a
            href="/report/2A202601256_report.md"
            target="_blank"
            className="inline-flex items-center gap-2 px-5 py-3 rounded-lg font-bold text-xs text-[#124f8c] bg-blue-50 border border-blue-200 hover:bg-blue-100 transition-colors"
          >
            <span>Tải Báo Cáo Markdown (2A202601256_report.md) →</span>
          </a>
          <a
            href="/Slide_Lab_Day11.html"
            target="_blank"
            className="inline-flex items-center gap-2 px-5 py-3 rounded-lg font-bold text-xs text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 transition-colors"
          >
            <span>Xem Slide Lab Day 11 →</span>
          </a>
        </div>
      </div>
    </section>
  );
}