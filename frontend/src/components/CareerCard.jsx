/**
 * components/CareerCard.jsx
 * -------------------------
 * Career recommendation card styled according to DESIGN.md.
 * Alternates between warm cream cards (#efe9de / #ffffff) and dark product
 * mockup surfaces (#181715) for technical roadmap steps.
 */

import React, { useState } from 'react';
import { 
  ChevronDown, 
  ChevronUp, 
  GraduationCap, 
  Target, 
  Check, 
  Terminal, 
  ArrowRight, 
  Sparkles, 
  BookOpen,
  Cpu
} from 'lucide-react';
import SkillList from './SkillList';

export default function CareerCard({ career, rank = 1 }) {
  const [showRoadmap, setShowRoadmap] = useState(rank === 1); // Expand top recommendation by default

  const score = career.matching_score || 0;
  const breakdown = career.score_breakdown || {};
  const roadmap = career.learning_roadmap || {};
  const missingSkills = career.missing_skills || [];
  const matchedSkills = career.matched_skills || [];

  const algoBullets = career.ai_algo_breakdown?.bullets || [
    `Skill Matching: Identified ${matchedSkills.length} acquired strength(s) (${breakdown.skill_match_percentage ?? 0}%) and predicted ${missingSkills.length} missing skill(s) for this track.`,
    `Multi-Factor Scoring: Combined 50% Skill Match + 30% Interest Match (${breakdown.interest_match_percentage ?? 0}%) + 20% Education (${breakdown.education_match_percentage ?? 0}%).`,
    `Roadmap Synthesis: Outlined step-by-step milestones to help acquire missing competencies.`
  ];

  // Determine progress bar and badge accent
  const isTopRank = rank === 1;

  return (
    <div className={`rounded-xl border transition-all duration-300 shadow-2xs overflow-hidden flex flex-col justify-between ${
      isTopRank 
        ? 'bg-[#ffffff] border-[#cc785c]/60 ring-2 ring-[#cc785c]/10' 
        : 'bg-[#ffffff] border-[#e6dfd8] hover:border-[#d6cbbe]'
    }`}>
      
      {/* Top Banner & Header */}
      <div className="p-6 sm:p-7">
        
        {/* Top Meta Line: Rank Badge & Match Score */}
        <div className="flex items-center justify-between gap-3 mb-4">
          
          <div className="flex items-center gap-2">
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold tracking-wide ${
              isTopRank
                ? 'bg-[#cc785c] text-white shadow-xs'
                : rank === 2
                ? 'bg-[#141413] text-[#faf9f5]'
                : 'bg-[#efe9de] text-[#3d3d3a] border border-[#e6dfd8]'
            }`}>
              <span>#{rank}</span>
              <span>{isTopRank ? 'Best Match' : 'High Fit'}</span>
            </span>

            {career.matches_career_goal && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-[#f5f0e8] text-[#cc785c] border border-[#e6dfd8]">
                <Sparkles className="w-3 h-3 text-[#cc785c]" />
                Goal Match
              </span>
            )}
          </div>

          {/* Match Score */}
          <div className="text-right">
            <div className="flex items-baseline justify-end gap-1">
              <span className="text-3xl font-editorial font-normal text-[#141413]">
                {score}%
              </span>
              <span className="text-[11px] font-semibold text-[#8e8b82] uppercase tracking-wider">
                Match
              </span>
            </div>
          </div>
        </div>

        {/* Career Title & Description */}
        <h3 className="text-2xl font-editorial text-[#141413] tracking-tight mb-2 leading-tight">
          {career.career_title}
        </h3>
        <p className="text-xs text-[#6c6a64] leading-relaxed mb-5">
          {career.description}
        </p>

        {/* Visual Progress Bar (Clean 6px bar) */}
        <div className="space-y-1.5 mb-6">
          <div className="w-full bg-[#f5f0e8] h-2 rounded-full overflow-hidden border border-[#e6dfd8]/60">
            <div
              className={`h-full rounded-full transition-all duration-700 ${
                isTopRank ? 'bg-[#cc785c]' : 'bg-[#5db872]'
              }`}
              style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
            />
          </div>
          <div className="flex justify-between items-center text-[11px] text-[#8e8b82] font-mono">
            <span>Overall Alignment</span>
            <span>{score} / 100</span>
          </div>
        </div>

        {/* Explainable 50/30/20 Breakdown Grid */}
        <div className="grid grid-cols-3 gap-2 p-3 bg-[#faf9f5] rounded-lg border border-[#e6dfd8] text-center mb-6">
          <div>
            <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Skills (50%)</div>
            <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">
              {breakdown.skill_match_percentage ?? 0}%
            </div>
          </div>
          <div className="border-x border-[#e6dfd8]">
            <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Interest (30%)</div>
            <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">
              {breakdown.interest_match_percentage ?? 0}%
            </div>
          </div>
          <div>
            <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Edu (20%)</div>
            <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">
              {breakdown.education_match_percentage ?? 0}%
            </div>
          </div>
        </div>

        {/* AI Algo Analysis Box for This Career */}
        <div className="bg-[#faf9f5] rounded-xl border border-[#e6dfd8] p-4 mb-6 space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#cc785c] flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-[#cc785c]" />
              AI Algo:- Skill Gap & Heuristic Match
            </span>
            <span className="text-[10px] font-mono font-medium text-[#8e8b82]">
              {score}% Match
            </span>
          </div>
          <ul className="text-xs text-[#55534e] space-y-1.5 pl-0.5">
            {algoBullets.map((bullet, bIdx) => (
              <li key={bIdx} className="flex items-start gap-2 leading-relaxed">
                <span className="text-[#cc785c] font-bold shrink-0 mt-0.5">•</span>
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Recommended Education Notice */}
        {career.recommended_education && (
          <div className="flex items-start gap-2.5 text-xs text-[#3d3d3a] bg-[#f5f0e8] border border-[#e6dfd8] p-3 rounded-lg mb-6">
            <GraduationCap className="w-4 h-4 text-[#cc785c] shrink-0 mt-0.5" />
            <div className="leading-snug">
              <span className="font-semibold text-[#141413]">Recommended Background: </span>
              <span>{career.recommended_education}</span>
            </div>
          </div>
        )}

        {/* Skill Gap Analysis Section */}
        <div className="space-y-4 pt-3 border-t border-[#e6dfd8]">
          
          {/* Matched Skills */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-[#141413] flex items-center gap-1.5">
                <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
                Acquired Competencies ({matchedSkills.length})
              </span>
            </div>
            <SkillList skills={matchedSkills} type="matched" emptyMessage="No overlap identified." />
          </div>

          {/* Missing Skills */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-[#cc785c] flex items-center gap-1.5">
                <Target className="w-3.5 h-3.5 text-[#cc785c]" />
                Target Competencies to Build ({missingSkills.length})
              </span>
            </div>
            <SkillList skills={missingSkills} type="missing" emptyMessage="All required competencies mastered." />
          </div>

        </div>

      </div>

      {/* Roadmap Section Footer with Dark Product Surface Contrast */}
      {missingSkills.length > 0 && (
        <div className="border-t border-[#e6dfd8] bg-[#faf9f5] rounded-b-xl p-4 sm:p-5">
          <button
            onClick={() => setShowRoadmap(!showRoadmap)}
            className="w-full flex items-center justify-between text-xs font-semibold text-[#141413] hover:text-[#cc785c] transition-colors py-1 cursor-pointer"
          >
            <span className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-[#cc785c]" />
              <span>{showRoadmap ? 'Hide Learning Roadmap' : `View Learning Roadmap (${missingSkills.length} skills)`}</span>
            </span>
            {showRoadmap ? <ChevronUp className="w-4 h-4 text-[#8e8b82]" /> : <ChevronDown className="w-4 h-4 text-[#8e8b82]" />}
          </button>

          {/* Expanded Dark Technical Code Window Container */}
          {showRoadmap && (
            <div className="mt-4 space-y-3 pt-3 border-t border-[#e6dfd8]">
              <p className="text-[11px] text-[#6c6a64] leading-relaxed">
                Step-by-step milestones retrieved from the knowledge base for closing your skill gaps:
              </p>

              {missingSkills.map((skillName) => {
                const steps = roadmap[skillName] || [];
                return (
                  <div 
                    key={skillName} 
                    className="bg-[#181715] text-[#faf9f5] p-3.5 rounded-lg border border-[#252320] shadow-xs"
                  >
                    <div className="flex items-center justify-between mb-2 pb-1.5 border-b border-[#252320]">
                      <span className="text-xs font-bold font-mono text-[#cc785c] flex items-center gap-1.5">
                        <Terminal className="w-3.5 h-3.5" />
                        {skillName}
                      </span>
                      <span className="text-[10px] font-mono text-[#8e8b82]">
                        {steps.length} Steps
                      </span>
                    </div>

                    <ol className="space-y-2 pl-0.5">
                      {steps.map((step, idx) => (
                        <li key={idx} className="text-xs text-[#faf9f5]/90 flex items-start gap-2 leading-relaxed">
                          <span className="font-mono text-[#8e8b82] text-[10px] mt-0.5 shrink-0">
                            0{idx + 1}.
                          </span>
                          <span>{step}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

    </div>
  );
}
