/**
 * pages/Home.jsx
 * --------------
 * Claude-inspired warm editorial landing page for CareerCompass AI.
 * Cream canvas (#faf9f5), Newsreader serif typography, coral CTAs (#cc785c),
 * light cream feature cards (#efe9de), and dark product surfaces (#181715).
 */

import React from 'react';
import { 
  ArrowRight, 
  Check, 
  Cpu, 
  Target, 
  BookOpen, 
  Sparkles, 
  ShieldCheck, 
  BarChart3, 
  Code2, 
  Globe,
  Sliders
} from 'lucide-react';

export default function Home({ onGetStarted }) {
  const steps = [
    {
      number: '01',
      title: 'Define Competency Profile',
      desc: 'Enter your academic degree, select skills you have acquired, and specify your authentic career interests.',
      icon: <Target className="w-5 h-5 text-[#cc785c]" />
    },
    {
      number: '02',
      title: 'Heuristic Rule-Based Matching',
      desc: 'Our explainable expert system evaluates your profile using 50% skill, 30% interest, and 20% education weights.',
      icon: <Sliders className="w-5 h-5 text-[#cc785c]" />
    },
    {
      number: '03',
      title: 'Actionable Skill Roadmaps',
      desc: 'Inspect exact gaps between your skillset and target careers, with structured milestones to master missing skills.',
      icon: <BookOpen className="w-5 h-5 text-[#cc785c]" />
    }
  ];

  const tracks = [
    { title: 'Software Developer', icon: <Code2 className="w-4 h-4 text-[#cc785c]" />, skills: 'Python, Java, DSA, Git, SQL' },
    { title: 'Web Developer', icon: <Globe className="w-4 h-4 text-[#5db8a6]" />, skills: 'HTML, CSS, React, Node.js, Git' },
    { title: 'Data Analyst', icon: <BarChart3 className="w-4 h-4 text-[#e8a55a]" />, skills: 'Python, SQL, Excel, Power BI, Statistics' },
    { title: 'AI/ML Engineer', icon: <Cpu className="w-4 h-4 text-[#cc785c]" />, skills: 'Python, ML, Deep Learning, Mathematics' },
    { title: 'Cybersecurity Analyst', icon: <ShieldCheck className="w-4 h-4 text-[#5db8a6]" />, skills: 'Network Security, Linux, Cryptography, SIEM' },
  ];

  return (
    <div className="space-y-20 py-10 sm:py-16">
      
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto px-4 space-y-6">
        
        {/* Category Pill Tag */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium bg-[#efe9de] text-[#141413] border border-[#e6dfd8] shadow-2xs">
          <Sparkles className="w-3.5 h-3.5 text-[#cc785c]" />
          <span>Explainable Rule-Based Career Intelligence</span>
        </div>

        {/* Editorial Serif Heading */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-editorial font-normal text-[#141413] tracking-tight leading-[1.08] max-w-3xl mx-auto">
          Discover your ideal career path with <span className="text-[#cc785c] italic">clarity & purpose.</span>
        </h1>

        {/* Subtitle */}
        <p className="text-base sm:text-lg text-[#6c6a64] max-w-2xl mx-auto leading-relaxed">
          A personalized career guidance system combining transparent heuristic scoring with 
          concrete skill gap analysis. No black-box algorithms — just explainable guidance.
        </p>

        {/* CTA Buttons */}
        <div className="pt-3 flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={onGetStarted}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3 rounded-lg font-medium text-sm text-white bg-[#cc785c] hover:bg-[#a9583e] active:bg-[#8f4730] transition-colors shadow-xs cursor-pointer"
          >
            <span>Find My Career</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Trust Points */}
        <div className="pt-3 flex flex-wrap items-center justify-center gap-6 text-xs text-[#8e8b82]">
          <span className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
            50% Skill • 30% Interest • 20% Education
          </span>
          <span className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
            Deterministic Heuristic Model
          </span>
          <span className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
            Full Skill Roadmap Generation
          </span>
        </div>

      </section>

      {/* 3-Step Process (Cream Cards) */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-10 space-y-2">
          <h2 className="text-3xl font-editorial font-normal text-[#141413]">
            How the System Works
          </h2>
          <p className="text-xs text-[#6c6a64] max-w-md mx-auto">
            A transparent 3-step evaluation model based on standard industry competency frameworks.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {steps.map((step) => (
            <div 
              key={step.number}
              className="bg-[#efe9de] p-7 sm:p-8 rounded-xl border border-[#e6dfd8] space-y-4 relative overflow-hidden"
            >
              <div className="text-3xl font-editorial text-[#d6cbbe] absolute top-5 right-6 select-none font-normal">
                {step.number}
              </div>
              <div className="w-10 h-10 rounded-lg bg-[#faf9f5] flex items-center justify-center border border-[#e6dfd8]">
                {step.icon}
              </div>
              <div>
                <h3 className="text-lg font-editorial font-normal text-[#141413] mb-1.5">
                  {step.title}
                </h3>
                <p className="text-xs text-[#6c6a64] leading-relaxed">
                  {step.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Supported Career Pathways (Dark Product Chrome) */}
      <section className="max-w-6xl mx-auto px-4 pb-4">
        <div className="bg-[#181715] text-[#faf9f5] rounded-2xl p-8 sm:p-10 border border-[#252320] shadow-sm">
          
          <div className="max-w-xl mb-8 space-y-1.5">
            <span className="text-[11px] font-mono text-[#cc785c] uppercase tracking-wider">
              Domain Competency Catalog
            </span>
            <h3 className="text-2xl font-editorial font-normal text-[#faf9f5]">
              Curated Technical Career Tracks
            </h3>
            <p className="text-xs text-[#a09d96] leading-relaxed">
              Every track defines required proficiencies, foundational degrees, and prerequisite frameworks.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {tracks.map((track) => (
              <div 
                key={track.title}
                className="bg-[#1f1e1b] border border-[#252320] p-4 rounded-xl flex items-start gap-3.5 hover:border-[#383531] transition-colors"
              >
                <div className="p-2 rounded-lg bg-[#252320] shrink-0 mt-0.5">
                  {track.icon}
                </div>
                <div>
                  <h4 className="font-medium text-sm text-[#faf9f5] mb-1">
                    {track.title}
                  </h4>
                  <p className="text-xs text-[#a09d96] font-mono text-[11px]">
                    {track.skills}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 pt-6 border-t border-[#252320] flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-[#a09d96]">
              Ready to evaluate your profile against all 5 tracks?
            </p>
            <button
              onClick={onGetStarted}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] transition-colors cursor-pointer"
            >
              <span>Start Evaluation</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

        </div>
      </section>

    </div>
  );
}
