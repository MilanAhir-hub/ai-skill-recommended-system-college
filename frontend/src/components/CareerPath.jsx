/**
 * components/CareerPath.jsx
 * -------------------------
 * Renders the generated career path for one career:
 *   1. Readiness meter   - where the student stands against the entry bar
 *   2. Learning timeline - prerequisite-ordered phases with week ranges
 *   3. Role ladder       - the 5-stage progression with salary bands
 *   4. Next actions      - what to literally do this week
 *
 * Styled with the DESIGN.md tokens: cream surfaces (#faf9f5 / #efe9de),
 * coral accents (#cc785c) and dark product surfaces (#2e2a26) for the
 * technical roadmap steps.
 */

import React, { useState } from 'react';
import {
  Route,
  Gauge,
  CalendarClock,
  TrendingUp,
  Terminal,
  Check,
  ChevronDown,
  ChevronUp,
  Link2,
  Rocket,
  Award,
  FolderGit2,
  Briefcase,
  IndianRupee,
  Clock,
  ArrowRight,
  Layers
} from 'lucide-react';

const DIFFICULTY_STYLES = {
  Beginner: 'bg-[#eef6ef] text-[#2f6b3c] border-[#d1e7d8]',
  Intermediate: 'bg-[#fdf4e7] text-[#8a5a12] border-[#f0e0c4]',
  Advanced: 'bg-[#fbeeea] text-[#a9452c] border-[#f0d8ce]'
};

const STATUS_STYLES = {
  entered: { label: 'You are here', dot: 'bg-[#5db872]', chip: 'bg-[#eef6ef] text-[#2f6b3c] border-[#d1e7d8]' },
  target: { label: 'Your target', dot: 'bg-[#cc785c]', chip: 'bg-[#f5f0e8] text-[#a9583e] border-[#f0d8ce]' },
  next: { label: 'Next step', dot: 'bg-[#e8a55a]', chip: 'bg-[#fdf4e7] text-[#8a5a12] border-[#f0e0c4]' },
  future: { label: 'Later', dot: 'bg-[#d6cbbe]', chip: 'bg-[#faf9f5] text-[#8e8b82] border-[#e6dfd8]' }
};

function ReadinessMeter({ readiness }) {
  const coverage = readiness?.skill_coverage_percentage ?? 0;

  return (
    <div className="bg-[#faf9f5] border border-[#e6dfd8] rounded-xl p-4 space-y-3">
      <div className="flex items-start justify-between gap-3">
        <span className="text-[11px] font-bold uppercase tracking-wider text-[#cc785c] flex items-center gap-1.5">
          <Gauge className="w-3.5 h-3.5" />
          Current Readiness
        </span>
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[#efe9de] text-[#141413] border border-[#e6dfd8]">
          {readiness?.level || 'Explorer'}
        </span>
      </div>

      <div className="space-y-1.5">
        <div className="w-full bg-[#efe9de] h-2 rounded-full overflow-hidden border border-[#e6dfd8]/60">
          <div
            className="h-full rounded-full bg-[#cc785c] transition-all duration-700"
            style={{ width: `${Math.min(100, Math.max(0, coverage))}%` }}
          />
        </div>
        <div className="flex justify-between text-[11px] font-mono text-[#8e8b82]">
          <span>Benchmark skill coverage</span>
          <span>{coverage}%</span>
        </div>
      </div>

      <p className="text-xs text-[#55534e] leading-relaxed">
        {readiness?.message}
      </p>

      {readiness?.blocking_core_skills?.length > 0 && (
        <div className="text-[11px] text-[#a9452c] bg-[#fbeeea] border border-[#f0d8ce] rounded-lg px-2.5 py-2 leading-relaxed">
          <span className="font-semibold">Must-have gaps: </span>
          {readiness.blocking_core_skills.join(', ')}
        </div>
      )}
    </div>
  );
}

function SkillBlock({ item }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="bg-[#2e2a26] text-[#faf9f5] rounded-lg border border-[#4a443d] overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-start justify-between gap-3 p-3 text-left hover:bg-[#3a3530] transition-colors cursor-pointer"
      >
        <div className="min-w-0 space-y-1.5">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-bold font-mono text-[#cc785c] flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5" />
              {item.skill}
            </span>
            {item.is_core_skill && (
              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-[#cc785c] text-white">
                Must-have
              </span>
            )}
            {item.is_bridge_skill && (
              <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-[#4a443d] text-[#c2bbb0] border border-[#5d554b] inline-flex items-center gap-1">
                <Link2 className="w-2.5 h-2.5" />
                Prerequisite
              </span>
            )}
          </div>
          <div className="flex items-center gap-2.5 text-[10px] font-mono text-[#8e8b82]">
            <span>{item.difficulty}</span>
            <span>~{item.learning_hours} hrs</span>
            <span>{item.steps?.length || 0} steps</span>
          </div>
        </div>
        {open
          ? <ChevronUp className="w-4 h-4 text-[#8e8b82] shrink-0 mt-1" />
          : <ChevronDown className="w-4 h-4 text-[#8e8b82] shrink-0 mt-1" />}
      </button>

      {open && (
        <div className="px-3 pb-3 space-y-3 border-t border-[#4a443d] pt-3">
          {item.prerequisites?.length > 0 && (
            <p className="text-[11px] text-[#c2bbb0] font-mono">
              Requires first: {item.prerequisites.join(', ')}
            </p>
          )}

          <ol className="space-y-2">
            {(item.steps || []).map((step, idx) => (
              <li key={idx} className="text-xs text-[#faf9f5]/90 flex items-start gap-2 leading-relaxed">
                <span className="font-mono text-[#8e8b82] text-[10px] mt-0.5 shrink-0">
                  0{idx + 1}.
                </span>
                <span>{step}</span>
              </li>
            ))}
          </ol>

          {item.resources?.length > 0 && (
            <div className="pt-2 border-t border-[#4a443d]">
              <p className="text-[10px] font-semibold uppercase tracking-wider text-[#8e8b82] mb-1.5">
                Free resources
              </p>
              <ul className="space-y-1">
                {item.resources.map((resource, idx) => (
                  <li key={idx} className="text-[11px] text-[#c2bbb0] flex items-start gap-1.5">
                    <span className="text-[#cc785c]">-</span>
                    <span>{resource}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function LearningTimeline({ plan }) {
  if (!plan?.phases?.length) {
    return (
      <div className="bg-[#eef6ef] border border-[#d1e7d8] rounded-xl p-4 text-xs text-[#2f6b3c] flex items-center gap-2">
        <Check className="w-4 h-4 stroke-[2.5]" />
        <span>You already cover every benchmark skill for this career. Focus on projects and interviews.</span>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Plan summary strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 p-3 bg-[#faf9f5] rounded-lg border border-[#e6dfd8] text-center">
        <div>
          <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Skills</div>
          <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">{plan.total_skills_to_learn}</div>
        </div>
        <div className="sm:border-l border-[#e6dfd8]">
          <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Study hrs</div>
          <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">{plan.total_learning_hours}</div>
        </div>
        <div className="border-l border-[#e6dfd8]">
          <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">At {plan.hours_per_week} hrs/wk</div>
          <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">{plan.estimated_weeks} wks</div>
        </div>
        <div className="border-l border-[#e6dfd8]">
          <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Timeline</div>
          <div className="text-sm font-bold text-[#141413] mt-0.5 font-mono">{plan.estimated_months} mo</div>
        </div>
      </div>

      {plan.bridge_skills?.length > 0 && (
        <p className="text-[11px] text-[#6c6a64] bg-[#f5f0e8] border border-[#e6dfd8] rounded-lg px-3 py-2 leading-relaxed">
          <span className="font-semibold text-[#141413]">Added automatically: </span>
          {plan.bridge_skills.join(', ')} - prerequisites the engine pulled in so the order actually works.
        </p>
      )}

      {/* Phases as a vertical timeline */}
      <ol className="relative space-y-4 pl-6 border-l-2 border-[#e6dfd8]">
        {plan.phases.map((phase) => (
          <li key={phase.display_phase} className="relative">
            <span className="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-[#cc785c] border-2 border-[#faf9f5]" />

            <div className="space-y-2.5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h5 className="text-sm font-semibold text-[#141413] flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-[#cc785c]" />
                  {phase.name}
                </h5>
                <span className="text-[10px] font-mono text-[#8e8b82] inline-flex items-center gap-1">
                  <CalendarClock className="w-3 h-3" />
                  Week {phase.starts_week}-{phase.ends_week}
                  {phase.estimated_hours > 0 && ` | ${phase.estimated_hours} hrs`}
                </span>
              </div>

              <p className="text-[11px] text-[#6c6a64] leading-relaxed">{phase.goal}</p>

              {phase.skills?.length > 0 && (
                <div className="space-y-2">
                  {phase.skills.map((item) => (
                    <SkillBlock key={item.skill} item={item} />
                  ))}
                </div>
              )}

              {phase.action_steps?.length > 0 && (
                <ul className="space-y-1.5 bg-[#efe9de] border border-[#e6dfd8] rounded-lg p-3">
                  {phase.action_steps.map((step, idx) => (
                    <li key={idx} className="text-xs text-[#3d3d3a] flex items-start gap-2 leading-relaxed">
                      <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5] shrink-0 mt-0.5" />
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              )}

              {phase.portfolio_projects?.length > 0 && (
                <div className="grid grid-cols-1 gap-2">
                  {phase.portfolio_projects.map((project, idx) => (
                    <div
                      key={idx}
                      className="text-xs text-[#3d3d3a] bg-[#faf9f5] border border-[#e6dfd8] rounded-lg px-3 py-2 flex items-start gap-2 leading-relaxed"
                    >
                      <FolderGit2 className="w-3.5 h-3.5 text-[#cc785c] shrink-0 mt-0.5" />
                      <span>{project}</span>
                    </div>
                  ))}
                </div>
              )}

              {phase.certifications?.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {phase.certifications.map((cert) => (
                    <span
                      key={cert}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-[#f5f0e8] text-[#3d3d3a] border border-[#e6dfd8]"
                    >
                      <Award className="w-3 h-3 text-[#cc785c]" />
                      {cert}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}

function RoleLadder({ ladder }) {
  if (!ladder?.length) return null;

  return (
    <div className="space-y-2.5">
      {ladder.map((stage) => {
        const style = STATUS_STYLES[stage.status] || STATUS_STYLES.future;
        const isHighlighted = stage.status === 'target' || stage.status === 'entered';

        return (
          <div
            key={stage.stage}
            className={`rounded-xl border p-3.5 transition-colors ${
              isHighlighted
                ? 'bg-[#f5f0e8] border-[#cc785c]/50'
                : 'bg-[#faf9f5] border-[#e6dfd8]'
            }`}
          >
            <div className="flex items-start justify-between gap-3 mb-1.5">
              <div className="flex items-start gap-2.5 min-w-0">
                <span className={`w-2.5 h-2.5 rounded-full shrink-0 mt-1.5 ${style.dot}`} />
                <div className="min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-[10px] font-mono text-[#8e8b82]">Stage {stage.stage}</span>
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded border ${style.chip}`}>
                      {style.label}
                    </span>
                  </div>
                  <h5 className="text-sm font-semibold text-[#141413] leading-snug mt-0.5">
                    {stage.role}
                  </h5>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-2 text-[11px] text-[#6c6a64] mb-2 pl-5">
              <span className="inline-flex items-center gap-1 bg-white px-2 py-0.5 rounded border border-[#e6dfd8]">
                <Clock className="w-3 h-3 text-[#8e8b82]" />
                {stage.experience}
              </span>
              <span className="inline-flex items-center gap-1 bg-white px-2 py-0.5 rounded border border-[#e6dfd8] font-mono">
                <IndianRupee className="w-3 h-3 text-[#8e8b82]" />
                {stage.salary_inr}
              </span>
            </div>

            <div className="pl-5 space-y-1.5">
              <p className="text-xs text-[#55534e] leading-relaxed">{stage.focus}</p>
              <p className="text-[11px] text-[#6c6a64] leading-relaxed">
                <span className="font-semibold text-[#141413]">Milestone: </span>
                {stage.milestone}
              </p>

              {stage.skills_to_add?.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-0.5">
                  {stage.skills_to_add.map((skill) => {
                    const owned = stage.skills_already_acquired?.includes(skill);
                    return (
                      <span
                        key={skill}
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium border ${
                          owned
                            ? 'bg-[#eef6ef] text-[#2f6b3c] border-[#d1e7d8]'
                            : 'bg-white text-[#3d3d3a] border-[#e6dfd8]'
                        }`}
                      >
                        {owned && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                        {skill}
                      </span>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default function CareerPath({ careerPath, defaultTab = 'plan' }) {
  const [tab, setTab] = useState(defaultTab);

  if (!careerPath) return null;

  const { readiness, learning_plan: plan, progression_ladder: ladder, next_actions: nextActions, market_insights: market } = careerPath;

  const tabs = [
    { id: 'plan', label: 'Learning Path', icon: <Route className="w-3.5 h-3.5" /> },
    { id: 'ladder', label: 'Role Growth', icon: <TrendingUp className="w-3.5 h-3.5" /> },
    { id: 'market', label: 'Field Insights', icon: <Briefcase className="w-3.5 h-3.5" /> }
  ];

  return (
    <div className="space-y-4">
      <ReadinessMeter readiness={readiness} />

      {/* Next actions: the single most useful block, always visible */}
      {nextActions?.length > 0 && (
        <div className="bg-[#efe9de] border border-[#e6dfd8] rounded-xl p-4 space-y-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#cc785c] flex items-center gap-1.5">
            <Rocket className="w-3.5 h-3.5" />
            Start this week
          </span>
          <ul className="space-y-1.5">
            {nextActions.map((action, idx) => (
              <li key={idx} className="text-xs text-[#3d3d3a] flex items-start gap-2 leading-relaxed">
                <ArrowRight className="w-3.5 h-3.5 text-[#cc785c] shrink-0 mt-0.5" />
                <span>{action}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Tab switcher */}
      <div className="flex items-center gap-1 p-1 bg-[#faf9f5] border border-[#e6dfd8] rounded-lg">
        {tabs.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`flex-1 inline-flex items-center justify-center gap-1.5 px-2 py-1.5 rounded-md text-[11px] font-semibold transition-colors cursor-pointer ${
              tab === item.id
                ? 'bg-[#141413] text-[#faf9f5]'
                : 'text-[#6c6a64] hover:bg-[#f5f0e8] hover:text-[#141413]'
            }`}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      {tab === 'plan' && <LearningTimeline plan={plan} />}

      {tab === 'ladder' && (
        <div className="space-y-3">
          <p className="text-[11px] text-[#6c6a64] leading-relaxed">
            Where this career goes after you land the first role, with indicative Indian salary bands:
          </p>
          <RoleLadder ladder={ladder} />
        </div>
      )}

      {tab === 'market' && market && (
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-[#faf9f5] border border-[#e6dfd8] rounded-lg p-3">
              <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Market demand</div>
              <div className="text-sm font-semibold text-[#141413] mt-0.5">{market.demand}</div>
            </div>
            <div className="bg-[#faf9f5] border border-[#e6dfd8] rounded-lg p-3">
              <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">Entry salary</div>
              <div className="text-sm font-semibold text-[#141413] mt-0.5 font-mono">{market.entry_salary_inr}</div>
            </div>
          </div>

          {market.growth_outlook && (
            <p className="text-xs text-[#55534e] leading-relaxed bg-[#f5f0e8] border border-[#e6dfd8] rounded-lg p-3">
              {market.growth_outlook}
            </p>
          )}

          {[
            { label: 'Hiring industries', values: market.industries },
            { label: 'Everyday tools', values: market.tools },
            { label: 'Soft skills that matter', values: market.soft_skills }
          ].map((group) => (
            group.values?.length > 0 && (
              <div key={group.label} className="space-y-1.5">
                <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">
                  {group.label}
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {group.values.map((value) => (
                    <span
                      key={value}
                      className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-white text-[#3d3d3a] border border-[#e6dfd8]"
                    >
                      {value}
                    </span>
                  ))}
                </div>
              </div>
            )
          ))}

          <div className="flex flex-wrap items-center gap-2 pt-1 text-[11px] text-[#6c6a64]">
            <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded border ${
              market.remote_friendly
                ? 'bg-[#eef6ef] text-[#2f6b3c] border-[#d1e7d8]'
                : 'bg-[#fdf4e7] text-[#8a5a12] border-[#f0e0c4]'
            }`}>
              {market.remote_friendly ? 'Remote friendly' : 'Mostly on-site'}
            </span>
          </div>
        </div>
      )}

      {/* Difficulty legend */}
      <div className="flex flex-wrap items-center gap-2 pt-1">
        {Object.keys(DIFFICULTY_STYLES).map((level) => (
          <span
            key={level}
            className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold border ${DIFFICULTY_STYLES[level]}`}
          >
            {level}
          </span>
        ))}
      </div>
    </div>
  );
}
