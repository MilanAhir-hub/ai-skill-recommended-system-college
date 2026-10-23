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
  Sparkles,
  Cpu,
  Route,
  Link2,
  Clock,
  IndianRupee,
  Flame
} from 'lucide-react';
import SkillList from './SkillList';
import CareerPath from './CareerPath';

export default function CareerCard({ career, rank = 1 }) {
  const [showPath, setShowPath] = useState(rank === 1); // Expand top recommendation by default

  const score = career.matching_score || 0;
  const breakdown = career.score_breakdown || {};
  const missingSkills = career.missing_skills || [];
  const matchedSkills = career.matched_skills || [];
  const impliedSkills = career.implied_skills || [];
  const careerPath = career.career_path || null;
  const plan = careerPath?.learning_plan || null;
  const market = careerPath?.market_insights || {};
  const entryStage = careerPath?.entry_stage || null;

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
        <div className="flex items-center gap-2 mb-1.5 flex-wrap">
          {career.career_category && (
            <span className="text-[10px] font-semibold uppercase tracking-wider text-[#8e8b82]">
              {career.career_category}
            </span>
          )}
          {market.demand && (
            <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-[#a9583e]">
              <Flame className="w-3 h-3" />
              {market.demand} demand
            </span>
          )}
        </div>
        <h3 className="text-2xl font-editorial text-[#141413] tracking-tight mb-2 leading-tight">
          {career.career_title}
        </h3>
        <p className="text-xs text-[#6c6a64] leading-relaxed mb-4">
          {career.description}
        </p>

        {/* Entry role + timeline snapshot generated from the career path */}
        {(entryStage || plan) && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-5">
            {entryStage && (
              <div className="bg-[#f5f0e8] border border-[#e6dfd8] rounded-lg px-3 py-2">
                <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">
                  Entry role
                </div>
                <div className="text-xs font-semibold text-[#141413] mt-0.5 leading-snug">
                  {entryStage.role}
                </div>
                <div className="text-[11px] text-[#6c6a64] font-mono mt-0.5 flex items-center gap-1">
                  <IndianRupee className="w-3 h-3" />
                  {entryStage.salary_inr}
                </div>
              </div>
            )}
            {plan && (
              <div className="bg-[#f5f0e8] border border-[#e6dfd8] rounded-lg px-3 py-2">
                <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">
                  Time to job ready
                </div>
                <div className="text-xs font-semibold text-[#141413] mt-0.5 leading-snug">
                  {plan.estimated_duration}
                </div>
                <div className="text-[11px] text-[#6c6a64] font-mono mt-0.5 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {plan.total_learning_hours} hrs at {plan.hours_per_week}/wk
                </div>
              </div>
            )}
          </div>
        )}

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
            {impliedSkills.length > 0 && (
              <p className="text-[11px] text-[#6c6a64] mt-2 flex items-start gap-1.5 leading-relaxed">
                <Link2 className="w-3 h-3 text-[#8e8b82] shrink-0 mt-0.5" />
                <span>
                  <span className="font-medium text-[#141413]">{impliedSkills.join(', ')}</span>
                  {' '}credited automatically as {impliedSkills.length > 1 ? 'prerequisites' : 'a prerequisite'} of the skills you already listed.
                </span>
              </p>
            )}
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

      {/* Generated Career Path Footer */}
      {careerPath && (
        <div className="border-t border-[#e6dfd8] bg-[#faf9f5] rounded-b-xl p-4 sm:p-5">
          <button
            onClick={() => setShowPath(!showPath)}
            className="w-full flex items-center justify-between text-xs font-semibold text-[#141413] hover:text-[#cc785c] transition-colors py-1 cursor-pointer"
          >
            <span className="flex items-center gap-2 text-left">
              <Route className="w-4 h-4 text-[#cc785c] shrink-0" />
              <span>
                {showPath
                  ? 'Hide Generated Career Path'
                  : `View Generated Career Path${plan?.total_skills_to_learn
                      ? ` (${plan.total_skills_to_learn} skills, ${plan.estimated_duration.toLowerCase()})`
                      : ''}`}
              </span>
            </span>
            {showPath
              ? <ChevronUp className="w-4 h-4 text-[#8e8b82] shrink-0" />
              : <ChevronDown className="w-4 h-4 text-[#8e8b82] shrink-0" />}
          </button>

          {showPath && (
            <div className="mt-4 pt-4 border-t border-[#e6dfd8]">
              <CareerPath careerPath={careerPath} />
            </div>
          )}
        </div>
      )}

    </div>
  );
}
