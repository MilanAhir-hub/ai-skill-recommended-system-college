/**
 * components/AlgorithmPicker.jsx
 * ------------------------------
 * Two ready-made algorithm combinations instead of four separate switches.
 * Each combo pairs one way of ranking careers with one way of ordering the
 * learning path:
 *
 *   Combo 1  Weighted MCDA   +  Topological Sort (Kahn)   <- default
 *   Combo 2  Decision Tree   +  Breadth-First Search
 *
 * The individual algorithms are still available through the API; this picker
 * just keeps the choice to one click. All option text is read from the
 * backend catalog, so it stays in step with career_data.py.
 */

import React, { useState } from 'react';
import {
  Cpu,
  Check,
  ChevronDown,
  ChevronUp,
  Scale,
  GitBranch,
  Layers,
  Network,
  Plus
} from 'lucide-react';

const ALGORITHM_ICONS = {
  mcda: <Scale className="w-4 h-4" />,
  decision_tree: <GitBranch className="w-4 h-4" />,
  topological: <Layers className="w-4 h-4" />,
  bfs: <Network className="w-4 h-4" />
};

/* Offline fallback: the backend declares the real list in career_data.py and
   serves it from GET /api/algorithms. */
const FALLBACK_COMBOS = [
  {
    id: 'balanced',
    label: 'Combo 1',
    tagline: 'Balanced scoring, syllabus-style order',
    scoring: 'mcda',
    path: 'topological',
    best_for: 'A fit score you can defend line by line, and one unambiguous next step.',
    default: true
  },
  {
    id: 'tree-bfs',
    label: 'Combo 2',
    tagline: 'Readable decisions, parallel levels',
    scoring: 'decision_tree',
    path: 'bfs',
    best_for: 'Seeing the reasoning as a path of questions, and what you can start today in parallel.',
    default: false
  }
];

function AlgorithmSummary({ option, icon }) {
  if (!option) return null;

  return (
    <div className="flex items-start gap-2.5">
      <span className="w-7 h-7 rounded-lg bg-white text-[#cc785c] border border-[#e6dfd8] flex items-center justify-center shrink-0">
        {icon}
      </span>
      <div className="min-w-0">
        <div className="text-xs font-semibold text-[#141413]">{option.name}</div>
        <p className="text-[11px] text-[#6c6a64] leading-relaxed mt-0.5">{option.one_line}</p>
      </div>
    </div>
  );
}

function AlgorithmDetail({ option }) {
  if (!option) return null;

  return (
    <div className="space-y-2">
      <p className="text-[11px] font-semibold text-[#141413]">{option.name}</p>

      <ol className="space-y-1">
        {option.how_it_works?.map((step, idx) => (
          <li key={idx} className="text-[11px] text-[#3d3d3a] flex items-start gap-1.5 leading-relaxed">
            <span className="font-mono text-[#8e8b82] shrink-0">{idx + 1}.</span>
            <span>{step}</span>
          </li>
        ))}
      </ol>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-wider text-[#2f6b3c] mb-1">Strengths</p>
          <ul className="space-y-1">
            {option.strengths?.map((item, idx) => (
              <li key={idx} className="text-[11px] text-[#55534e] flex items-start gap-1.5 leading-relaxed">
                <span className="text-[#5db872]">+</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-wider text-[#a9452c] mb-1">Limits</p>
          <ul className="space-y-1">
            {option.limits?.map((item, idx) => (
              <li key={idx} className="text-[11px] text-[#55534e] flex items-start gap-1.5 leading-relaxed">
                <span className="text-[#c64545]">-</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function ComboCard({ combo, scoringOption, pathOption, selected, onSelect }) {
  const [open, setOpen] = useState(false);

  return (
    <div
      className={`rounded-xl border transition-all ${
        selected
          ? 'bg-[#f5f0e8] border-[#cc785c]/60 ring-2 ring-[#cc785c]/10'
          : 'bg-[#faf9f5] border-[#e6dfd8] hover:border-[#cc785c]/40'
      }`}
    >
      <button
        type="button"
        onClick={() => onSelect(combo)}
        className="w-full text-left p-4 cursor-pointer"
      >
        <div className="flex items-start gap-2.5 mb-3">
          <span
            className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 border font-mono text-[11px] font-bold ${
              selected
                ? 'bg-[#cc785c] text-white border-[#cc785c]'
                : 'bg-white text-[#cc785c] border-[#e6dfd8]'
            }`}
          >
            {selected ? <Check className="w-4 h-4 stroke-[2.5]" /> : combo.label.replace('Combo ', '')}
          </span>

          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm font-semibold text-[#141413]">{combo.label}</span>
            </div>
            <p className="text-[11px] text-[#6c6a64] leading-relaxed mt-0.5">{combo.tagline}</p>
          </div>
        </div>

        {/* The pair */}
        <div className="space-y-2.5 bg-white/60 rounded-lg border border-[#e6dfd8] p-3">
          <AlgorithmSummary
            option={scoringOption}
            icon={ALGORITHM_ICONS[combo.scoring] || <Cpu className="w-4 h-4" />}
          />
          <div className="flex items-center gap-2 pl-1">
            <Plus className="w-3 h-3 text-[#8e8b82]" />
            <span className="h-px flex-1 bg-[#e6dfd8]" />
          </div>
          <AlgorithmSummary
            option={pathOption}
            icon={ALGORITHM_ICONS[combo.path] || <Cpu className="w-4 h-4" />}
          />
        </div>

        <p className="text-[11px] text-[#55534e] leading-relaxed mt-2.5">
          <span className="font-semibold text-[#141413]">Best for: </span>
          {combo.best_for}
        </p>
      </button>

      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 pb-3 text-[11px] font-medium text-[#6c6a64] hover:text-[#141413] transition-colors cursor-pointer"
      >
        <span>{open ? 'Hide details' : 'How both work, strengths & limits'}</span>
        {open ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>

      {open && (
        <div className="px-4 pb-4 space-y-3 border-t border-[#e6dfd8] pt-3">
          <AlgorithmDetail option={scoringOption} />
          <div className="border-t border-[#e6dfd8] pt-3">
            <AlgorithmDetail option={pathOption} />
          </div>
          {scoringOption?.score_scale && (
            <p className="text-[10px] font-mono text-[#8e8b82] pt-1 border-t border-[#e6dfd8]">
              Score scale: {scoringOption.score_scale}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default function AlgorithmPicker({
  catalog,
  scoringAlgorithm,
  pathAlgorithm,
  onChangeCombo
}) {
  if (!catalog) return null;

  const findOption = (family, id) =>
    (catalog[family] || []).find((entry) => entry.id === id) || null;

  const combos = catalog.combos?.length ? catalog.combos : FALLBACK_COMBOS;

  return (
    <div className="bg-white rounded-xl border border-[#e6dfd8] p-6 sm:p-8 shadow-2xs space-y-5">
      <div className="space-y-1.5">
        <h2 className="text-2xl font-editorial font-normal text-[#141413] flex items-center gap-2">
          <Cpu className="w-5 h-5 text-[#cc785c]" />
          Choose the AI Algorithm
        </h2>
        <p className="text-xs text-[#6c6a64] leading-relaxed max-w-3xl">
          The same profile and the same knowledge base, reasoned over in two different ways. Each
          combination pairs a method for ranking careers with a method for ordering the learning
          path, and recalculates instantly. Both are deterministic and rule-based, so nothing here
          is trained or guessed.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {combos.map((combo) => (
          <ComboCard
            key={combo.id}
            combo={combo}
            scoringOption={findOption('scoring_algorithms', combo.scoring)}
            pathOption={findOption('path_algorithms', combo.path)}
            selected={scoringAlgorithm === combo.scoring && pathAlgorithm === combo.path}
            onSelect={onChangeCombo}
          />
        ))}
      </div>
    </div>
  );
}
