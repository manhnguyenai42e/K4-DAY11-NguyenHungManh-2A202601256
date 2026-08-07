"use client";

import { Shield, FileText, Github, ExternalLink } from "lucide-react";

export default function AcademicFooter() {
  return (
    <footer id="report" className="py-16 bg-[#0b192c] text-slate-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          <div className="lg:col-span-5">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#124f8c] to-[#38bdf8] text-white flex items-center justify-center">
                <Shield className="w-5 h-5" />
              </div>
              <div className="leading-tight">
                <div className="text-sm font-black text-white tracking-tight">
                  Guardrails &amp; HITL Dashboard
                </div>
                <div className="text-[11px] text-slate-400">Lab Day 11 · Responsible AI</div>
              </div>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              Portfolio demo thể hiện hệ thống multi-layer guardrails trên assistant ngân hàng,
              đo khả năng chống prompt-injection &amp; bypass, và thiết kế human-in-the-loop cho
              quyết định rủi ro cao. Sinh viên — 2A202601256.
            </p>
          </div>

          <div className="lg:col-span-4">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
              Báo cáo
            </div>
            <div className="space-y-2.5">
              <a
                href="/report/2A202601256_report.md"
                target="_blank"
                className="flex items-center gap-2 text-sm text-slate-300 hover:text-white transition-colors"
              >
                <FileText className="w-4 h-4 text-[#38bdf8]" /> report/2A202601256_report.md
                <ExternalLink className="w-3 h-3 text-slate-500" />
              </a>
              <a
                href="/Slide_Lab_Day11.html"
                target="_blank"
                className="flex items-center gap-2 text-sm text-slate-300 hover:text-white transition-colors"
              >
                <FileText className="w-4 h-4 text-[#38bdf8]" /> Slide_Lab_Day11.html
                <ExternalLink className="w-3 h-3 text-slate-500" />
              </a>
            </div>
          </div>

          <div className="lg:col-span-3">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
              Nguồn
            </div>
            <a
              href="https://github.com/"
              target="_blank"
              className="flex items-center gap-2 text-sm text-slate-300 hover:text-white transition-colors"
            >
              <Github className="w-4 h-4" /> GitHub Repo
            </a>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-500">
          <span>© 2026 Guardrails &amp; HITL Dashboard · Responsible AI</span>
          <span className="font-mono">Google ADK · Gemini · Tailwind · Next.js</span>
        </div>
      </div>
    </footer>
  );
}