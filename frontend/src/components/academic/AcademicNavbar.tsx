"use client";

import { useState } from "react";
import Link from "next/link";

const LINKS = [
  { href: "#abstract", label: "Abstract" },
  { href: "#architecture", label: "Pipeline" },
  { href: "#attacks", label: "Ma Trận Attack" },
  { href: "#metrics", label: "Metrics" },
  { href: "#hitl", label: "HITL Design" },
  { href: "#report", label: "Báo Cáo" },
];

export default function AcademicNavbar() {
  const [open, setOpen] = useState(false);

  const handleScrollClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault();
    setOpen(false);

    if (href === "#top") {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    const target = document.querySelector(href);
    if (target) {
      const navbarHeight = 64; // height of sticky header (h-16)
      const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight;
      window.scrollTo({
        top: Math.max(0, targetPosition),
        behavior: "smooth",
      });
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <a href="#top" onClick={(e) => handleScrollClick(e, "#top")} className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-[#124f8c] text-white flex items-center justify-center font-bold text-xs">
            VB
          </div>
          <div className="leading-tight">
            <div className="text-sm font-bold text-slate-900 tracking-tight">
              Guardrails &amp; HITL Dashboard
            </div>
            <div className="text-[11px] font-mono text-slate-500">Lab Day 11 · Responsible AI</div>
          </div>
        </a>

        <div className="hidden md:flex items-center gap-4">
          <nav className="flex items-center gap-1">
            {LINKS.map((l) => (
              <a
                key={l.label}
                href={l.href}
                onClick={(e) => handleScrollClick(e, l.href)}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-[#124f8c] hover:bg-slate-50 transition-colors"
              >
                {l.label}
              </a>
            ))}
          </nav>

          <Link
            href="/chat"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg font-bold text-xs text-white bg-[#124f8c] hover:bg-[#0b355f] transition-colors shadow-xs"
          >
            <span>Mở Chatbot Live (/chat) →</span>
          </Link>
        </div>

        <button
          className="md:hidden px-3 py-1.5 rounded-lg text-xs font-semibold border border-slate-200 text-slate-700"
          onClick={() => setOpen((v) => !v)}
          aria-label="Menu"
        >
          {open ? "Đóng Menu" : "Menu"}
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 py-3 space-y-1">
          {LINKS.map((l) => (
            <a
              key={l.label}
              href={l.href}
              onClick={(e) => handleScrollClick(e, l.href)}
              className="block px-3 py-2 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50"
            >
              {l.label}
            </a>
          ))}
          <Link
            href="/chat"
            onClick={() => setOpen(false)}
            className="block px-3 py-2.5 rounded-lg text-xs font-bold text-white bg-[#124f8c] text-center mt-2"
          >
            Mở Chatbot Live (/chat) →
          </Link>
        </div>
      )}
    </header>
  );
}