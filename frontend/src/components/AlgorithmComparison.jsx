/**
 * components/AlgorithmComparison.jsx
 * ----------------------------------
 * The "if we choose this one, then what?" view, compared at combo level.
 *
 * Each combo is run as a whole: scored by its own algorithm, with its path
 * built for its own top career. The result shows which career each combo
 * puts first, whether they agree, how the learning is shaped, and which
 * choice suits which situation.
 */

import React from 'react';
import {
  Scale,
  GitBranch,
  Layers,
  Network,
  Check,
  AlertTriangle,
  Loader2,
  RotateCcw,
  Trophy,
  Lightbulb,
  Clock,
  ListOrdered
} from 'lucide-react';

const ICONS = {
  mcda: <Scale className="w-3.5 h-3.5 text-[#cc785c]" />,
  decision_tree: <GitBranch className="w-3.5 h-3.5 text-[#cc785c]" />,
  topological: <Layers className="w-3.5 h-3.5 text-[#cc785c]" />,
  bfs: <Network className="w-3.5 h-3.5 text-[#cc785c]" />
};

function ComboResult({ combo, isActive, onChoose }) {
  return (
    <div
      className={`rounded-xl border p-4 space-y-3 ${
        isActive
          ? 'bg-[#f5f0e8] border-[#cc785c]/60 ring-2 ring-[#cc785c]/10'
          : 'bg-[#faf9f5] border-[#e6dfd8]'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-semibold text-[#141413]">{combo.label}</span>
            {isActive && (
              <span className="text-[10px] font-semibold text-[#2f6b3c]">In use</span>
            )}
          </div>
          <p className="text-[11px] text-[#6c6a64] mt-0.5">{combo.tagline}</p>
        </div>
      </div>

      {/* The pair */}
      <div className="flex flex-wrap items-center gap-1.5 text-[11px]">
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-white border border-[#e6dfd8] text-[#3d3d3a]">
          {ICONS[combo.scoring.id]}
          {combo.scoring.name}
        </span>
        <span className="text-[#8e8b82]">+</span>
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-white border border-[#e6dfd8] text-[#3d3d3a]">
          {ICONS[combo.path.id]}
          {combo.path.name}
        </span>
      </div>

      {/* What it picks */}
      <div className="bg-white rounded-lg border border-[#e6dfd8] p-2.5">
        <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">
          Picks first
        </div>
        <div className="text-sm font-semibold text-[#141413] leading-snug mt-0.5">
          {combo.top_career}
        </div>
        <div className="text-[11px] font-mono text-[#6c6a64] mt-0.5">
          {combo.top_score} - {combo.scoring.score_label}
        </div>
      </div>

      {/* Ranking */}
      <ol className="space-y-1">
        {(combo.ranking || []).map((row) => (
          <li
            key={row.career_id}
            className="flex items-center justify-between gap-2 text-[11px] text-[#3d3d3a]"
          >
            <span className="truncate">
              <span className="font-mono text-[#8e8b82] mr-1.5">{row.rank}.</span>
              {row.career_title}
            </span>
            <span className="font-mono text-[#6c6a64] shrink-0">{row.score}</span>
          </li>
        ))}
      </ol>

      {/* The plan it produces */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-white rounded-lg border border-[#e6dfd8] p-2">
          <div className="text-[10px] text-[#8e8b82] uppercase tracking-wider">Skills</div>
          <div className="text-sm font-bold font-mono text-[#141413]">{combo.plan.total_skills}</div>
        </div>
        <div className="bg-white rounded-lg border border-[#e6dfd8] p-2">
          <div className="text-[10px] text-[#8e8b82] uppercase tracking-wider">Hours</div>
          <div className="text-sm font-bold font-mono text-[#141413]">{combo.plan.total_hours}</div>
        </div>
        <div className="bg-white rounded-lg border border-[#e6dfd8] p-2">
          <div className="text-[10px] text-[#8e8b82] uppercase tracking-wider">
            {combo.path.phase_label}s
          </div>
          <div className="text-sm font-bold font-mono text-[#141413]">{combo.plan.group_count}</div>
        </div>
      </div>

      <div>
        <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider mb-1 flex items-center gap-1">
          <ListOrdered className="w-3 h-3" />
          First {combo.path.phase_label.toLowerCase()}: start with
        </div>
        <div className="flex flex-wrap gap-1.5">
          {(combo.plan.first_group || []).map((skill) => (
            <span
              key={skill}
              className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-white text-[#3d3d3a] border border-[#e6dfd8]"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      <p className="text-[11px] text-[#6c6a64] leading-relaxed flex items-start gap-1.5">
        <Clock className="w-3 h-3 shrink-0 mt-0.5" />
        <span>{combo.plan.estimated_duration} at your current study pace</span>
      </p>

      <p className="text-[11px] text-[#55534e] leading-relaxed border-t border-[#e6dfd8] pt-2">
        <span className="font-semibold text-[#141413]">Best for: </span>
        {combo.best_for}
      </p>

      <button
        onClick={() => onChoose(combo)}
        disabled={isActive}
        className={`w-full px-3 py-1.5 rounded-md text-[11px] font-semibold transition-colors ${
          isActive
            ? 'bg-[#efe9de] text-[#8e8b82] cursor-default'
            : 'bg-[#141413] text-[#faf9f5] hover:bg-[#252523] cursor-pointer'
        }`}
      >
        {isActive ? 'Currently selected' : `Use ${combo.label}`}
      </button>
    </div>
  );
}

export default function AlgorithmComparison({
  comparison,
  loading,
  error,
  onRun,
  activeScoring,
  activePath,
  onChooseCombo
}) {
  const combos = comparison?.combos || [];
  const agree =
    combos.length === 2 && combos[0].top_career_id === combos[1].top_career_id;

  return (
    <div className="bg-white rounded-xl border border-[#e6dfd8] p-6 sm:p-8 shadow-2xs space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="space-y-1.5">
          <h2 className="text-2xl font-editorial font-normal text-[#141413] flex items-center gap-2">
            <Trophy className="w-5 h-5 text-[#cc785c]" />
            If I choose this one, then what?
          </h2>
          <p className="text-xs text-[#6c6a64] leading-relaxed max-w-2xl">
            Runs both combinations on your profile and shows exactly what each choice would change.
          </p>
        </div>

        <button
          onClick={onRun}
          disabled={loading}
          className="shrink-0 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] transition-colors shadow-xs disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
        >
          {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <RotateCcw className="w-3.5 h-3.5" />}
          <span>{comparison ? 'Re-run comparison' : 'Compare both combos'}</span>
        </button>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2">
          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {!comparison && !loading && !error && (
        <p className="text-xs text-[#8e8b82] italic">
          Not run yet. Press the button to score your profile with both combinations.
        </p>
      )}

      {combos.length > 0 && (
        <div className="space-y-5">
          {/* Verdict */}
          {comparison.combo_verdict && (
            <div
              className={`rounded-xl border p-4 flex items-start gap-2.5 ${
                agree ? 'bg-[#eef6ef] border-[#d1e7d8]' : 'bg-[#fdf4e7] border-[#f0e0c4]'
              }`}
            >
              {agree
                ? <Check className="w-4 h-4 text-[#2f6b3c] stroke-[2.5] shrink-0 mt-0.5" />
                : <AlertTriangle className="w-4 h-4 text-[#8a5a12] shrink-0 mt-0.5" />}
              <p className="text-xs text-[#3d3d3a] leading-relaxed">{comparison.combo_verdict}</p>
            </div>
          )}

          {/* The two combos side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {combos.map((combo) => (
              <ComboResult
                key={combo.id}
                combo={combo}
                isActive={activeScoring === combo.scoring.id && activePath === combo.path.id}
                onChoose={onChooseCombo}
              />
            ))}
          </div>

          {/* How to choose */}
          <div className="bg-[#efe9de] border border-[#e6dfd8] rounded-xl p-4 space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#cc785c] flex items-center gap-1.5">
              <Lightbulb className="w-3.5 h-3.5" />
              Which should I pick?
            </span>
            <ul className="space-y-1.5">
              {(comparison.how_to_choose || []).slice(0, 2).map((line, idx) => (
                <li key={idx} className="text-xs text-[#3d3d3a] flex items-start gap-2 leading-relaxed">
                  <span className="text-[#cc785c] font-bold shrink-0">-</span>
                  <span>{line}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
