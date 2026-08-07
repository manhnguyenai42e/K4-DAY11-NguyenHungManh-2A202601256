"use client";

import { Fragment, useState } from "react";
import { AUDIT_LOG } from "@/lib/day11-data";

type AuditRow = {
  request_id: string;
  user_id?: string;
  timestamp?: string;
  input: string;
  output?: string;
  blocked: boolean;
  blocked_by_layer?: string | null;
  latency_ms?: number;
};

const rows = AUDIT_LOG as unknown as AuditRow[];

export default function HitlSection() {
  const [openRow, setOpenRow] = useState<number | null>(null);

  return (
    <section
      id="hitl"
      className="h-[calc(100vh-64px)] flex flex-col justify-center py-4 bg-white border-b border-slate-200 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        {/* Title */}
        <div className="max-w-3xl mx-auto text-center mb-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-blue-50 text-[#124f8c] border border-blue-200 text-[11px] font-bold uppercase tracking-wider mb-1">
            Human-in-the-Loop &amp; Audit
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
            Nhật Ký Audit &amp; Giám Sát Quyết Định
          </h2>
        </div>

        {/* 3 Router decision cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
          {[
            { title: "Tự Động Gửi (Auto-Approve)", cond: "confidence ≥ 0.90 / An toàn", action: "Cho phép trả về khách hàng trực tiếp", color: "border-[#124f8c] bg-blue-50/50 text-[#124f8c]" },
            { title: "Dual-Sync Telegram HITL", cond: "Giao dịch giá trị lớn (Ví dụ: Chuyển 100M VND)", action: "Gửi Ticket tới Telegram Admin Bot + Web Dashboard", color: "border-amber-300 bg-amber-50/50 text-amber-800" },
            { title: "Chặn & Từ Chối (Block & Escalate)", cond: "Prompt Injection / Violation", action: "Chặn ngay lập tức & ghi log giám sát", color: "border-red-300 bg-red-50/50 text-red-800" },
          ].map((c, idx) => (
            <div key={idx} className={`p-3 rounded-xl border ${c.color} shadow-xs text-xs space-y-1`}>
              <div className="font-bold text-slate-900">{c.title}</div>
              <div className="font-mono text-[10px] text-slate-600">Điều kiện: {c.cond}</div>
              <div className="text-[11px] font-medium text-slate-700">{c.action}</div>
            </div>
          ))}
        </div>

        {/* Audit Log Table */}
        <div className="academic-card rounded-xl overflow-hidden bg-white border border-slate-200 shadow-xs">
          <div className="overflow-x-auto max-h-[260px] overflow-y-auto">
            <table className="w-full text-xs">
              <thead className="sticky top-0 z-10 bg-slate-100 border-b border-slate-200">
                <tr className="text-left uppercase font-bold text-slate-500">
                  <th className="px-3 py-2">Request</th>
                  <th className="px-3 py-2 w-28">Trạng thái</th>
                  <th className="px-3 py-2">Lớp chặn</th>
                  <th className="px-3 py-2 w-1/2">Input</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {rows.slice(0, 12).map((r, i) => {
                  const open = openRow === i;
                  return (
                    <Fragment key={i}>
                      <tr
                        onClick={() => setOpenRow(open ? null : i)}
                        className="cursor-pointer hover:bg-slate-50 transition-colors"
                      >
                        <td className="px-3 py-2 font-mono text-[11px] text-slate-400">
                          {r.user_id || r.request_id}
                        </td>
                        <td className="px-3 py-2">
                          {r.blocked ? (
                            <span className="px-2 py-0.5 rounded bg-red-100 text-red-700 text-[10px] font-bold uppercase">
                              BLOCKED
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded bg-[#124f8c] text-white text-[10px] font-bold uppercase">
                              PASSED
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2 font-mono text-slate-700 font-semibold">
                          {r.blocked_by_layer || "—"}
                        </td>
                        <td className="px-3 py-2 text-slate-600 font-mono truncate max-w-xs">{r.input}</td>
                      </tr>
                      {open && (
                        <tr key={`${i}-det`}>
                          <td colSpan={4} className="px-4 py-2.5 bg-slate-50/90 text-xs border-y border-slate-200">
                            <div className="space-y-1 font-mono">
                              <div className="font-bold text-slate-900">Chi tiết Audit Row:</div>
                              <div className="text-[11px] text-slate-700">Latency: {r.latency_ms ?? 0}ms | Time: {r.timestamp ?? "N/A"}</div>
                              <pre className="p-2 rounded bg-white border border-slate-200 text-[11px] text-slate-800 whitespace-pre-wrap">
                                Input: {r.input}
                              </pre>
                            </div>
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}