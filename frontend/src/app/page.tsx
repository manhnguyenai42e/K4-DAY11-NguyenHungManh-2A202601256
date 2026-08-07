"use client";

import AcademicNavbar from "@/components/academic/AcademicNavbar";
import AcademicHero from "@/components/academic/AcademicHero";
import ResearchAbstract from "@/components/academic/ResearchAbstract";
import PipelineArchitecture from "@/components/academic/PipelineArchitecture";
import AttackResults from "@/components/academic/AttackResults";
import MetricsSection from "@/components/academic/MetricsSection";
import HitlSection from "@/components/academic/HitlSection";
import AcademicFooter from "@/components/academic/AcademicFooter";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans antialiased selection:bg-[#124f8c] selection:text-white">
      <AcademicNavbar />

      <main>
        <AcademicHero />
        <ResearchAbstract />
        <PipelineArchitecture />
        <AttackResults />
        <MetricsSection />
        <HitlSection />
      </main>

      <AcademicFooter />
    </div>
  );
}