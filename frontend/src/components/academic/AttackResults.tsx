"use client";

import { useState, Fragment } from "react";
import { ATTACK_RESULTS } from "@/lib/day11-data";

type Attack = {
  id: number;
  category: string;
  input: string;
};

type Row = {
  id: number;
  name: string;
  input: string;
  leaked: boolean;
};

const rawAttacks = (ATTACK_RESULTS as unknown as { unsafe_attacks: Attack[] }).unsafe_attacks || [];

const attacks: Row[] = rawAttacks.map((a) => ({
  id: a.id,
  name: a.category,
  input: a.input,
  leaked: true,
}));

const guardsRows: Row[] = attacks.map((a) => ({
  ...a,
  leaked: false,
}));

export default function AttackResults() {
  const [openRow, setOpenRow] = useState<number | null>(null);
  const [showGuards, setShowGuards] = useState(false);

  const rows: Row[] = showGuards
    ? guardsRows
    : attacks.map((a) => ({ ...a, leaked: true }));

  const leakCount = rows.filter((r) => r.leaked).length;

  return (
    <section
      id="attacks"
      className="h-[calc(100vh-64px)] flex flex-col justify-center py-4 bg-white border-b border-slate-200 overflow-hidden"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        {/* Title */}
        <div className="max-w-3xl mx-auto text-center mb-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-blue-50 text-[#124f8c] border border-blue-200 text-[11px] font-bold uppercase tracking-wider mb-1">
            Attack Leakage Matrix
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
            Ma Trận Kết Quả Attack (15 Vectors)
          </h2>
        </div>

        {/* Controls bar */}
        <div className="flex items-center justify-between gap-3 mb-3 bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <div className="flex items-center gap-4 text-xs font-semibold">
            <div className="flex items-center gap-1.5 text-slate-900 font-bold">
              <span>Tổng Attack:</span>
              <span className="px-2 py-0.5 rounded bg-slate-200 font-mono">{attacks.length}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="text-slate-500">Rò rỉ (Unsafe):</span>
              <span className={`px-2 py-0.5 rounded font-bold font-mono ${leakCount > 0 ? "bg-red-100 text-red-700" : "bg-emerald-100 text-emerald-800"}`}>
                {leakCount}/15
              </span>
            </div>
          </div>

          {/* Toggle */}
          <div className="inline-flex p-1 rounded-lg bg-slate-200/80 text-xs font-bold">
            <button
              onClick={() => setShowGuards(false)}
              className={`px-3 py-1 rounded-md transition-all ${
                !showGuards ? "bg-white text-red-700 shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Unsafe (Không Guardrails)
            </button>
            <button
              onClick={() => setShowGuards(true)}
              className={`px-3 py-1 rounded-md transition-all ${
                showGuards ? "bg-[#124f8c] text-white shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Guarded (Có Guardrails)
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="academic-card rounded-xl overflow-hidden bg-white border border-slate-200 shadow-xs">
          <div className="overflow-x-auto max-h-[360px] overflow-y-auto">
            <table className="w-full text-xs">
              <thead className="sticky top-0 z-10 bg-slate-100 border-b border-slate-200">
                <tr className="text-left uppercase font-bold text-slate-500">
                  <th className="px-3 py-2 w-12">#</th>
                  <th className="px-3 py-2 w-1/3">Vector Name</th>
                  <th className="px-3 py-2 w-28">Kết quả</th>
                  <th className="px-3 py-2">Input Prompt</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {rows.map((r, i) => {
                  const open = openRow === i;
                  return (
                    <Fragment key={`${i}-frag`}>
                      <tr
                        onClick={() => setOpenRow(open ? null : i)}
                        className="cursor-pointer hover:bg-slate-50 transition-colors"
                      >
                        <td className="px-3 py-2 font-mono text-slate-400 font-semibold">{i + 1}</td>
                        <td className="px-3 py-2 font-semibold text-slate-900">{r.name}</td>
                        <td className="px-3 py-2">
                          {r.leaked ? (
                            <span className="px-2 py-0.5 rounded bg-red-100 text-red-700 text-[10px] font-bold uppercase">
                              LEAKED
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded bg-[#124f8c] text-white text-[10px] font-bold uppercase">
                              BLOCKED
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-2 text-slate-600 font-mono truncate max-w-xs">{r.input}</td>
                      </tr>
                      {open && (
                        <tr key={`${i}-det`}>
                          <td colSpan={4} className="px-4 py-2.5 bg-slate-50/90 text-xs border-y border-slate-200">
                            <div className="space-y-1">
                              <div className="font-bold text-slate-900">Chi tiết Input Prompt Full:</div>
                              <pre className="p-2 rounded bg-white border border-slate-200 text-[11px] font-mono text-slate-800 whitespace-pre-wrap">
                                {r.input}
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