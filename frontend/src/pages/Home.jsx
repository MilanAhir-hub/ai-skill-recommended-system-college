/**
 * pages/Home.jsx
 * --------------
 * Claude-inspired warm editorial landing page for CareerCompass AI.
 * The hero counters, career catalog and in-demand skill list are all read
 * live from the backend knowledge base, so the page always reflects the
 * real contents of career_data.py instead of a hardcoded summary.
 */
import React, { useState, useEffect, useMemo } from 'react';
import {
  ArrowRight,
  Check,
  Cpu,
  Target,
  Sparkles,
  Sliders,
  Route,
  GitBranch,
  CalendarClock,
  TrendingUp,
  Flame,
  IndianRupee,
  Search,
  Layers,
  Scale,
  Network,
  Plus
} from 'lucide-react';
import {
  fetchKnowledgeBaseStats,
  fetchCareersCatalog,
  fetchAlgorithmCatalog
} from '../services/api';

/* Fallback counters so the page still reads correctly offline */
const FALLBACK_STATS = {
  total_careers: 21,
  total_skills: 92,
  total_career_stages: 105,
  total_roadmap_steps: 294,
  total_skill_aliases: 242
};

/* Shown if the backend is unreachable; the real list comes from /api/algorithms */
const FALLBACK_COMBOS = [
  {
    id: 'balanced',
    label: 'Combo 1',
    tagline: 'Balanced scoring, syllabus-style order',
    scoring: 'mcda',
    path: 'topological',
    best_for: 'A fit score you can defend line by line, and one unambiguous next step.'
  },
  {
    id: 'tree-bfs',
    label: 'Combo 2',
    tagline: 'Readable decisions, parallel levels',
    scoring: 'decision_tree',
    path: 'bfs',
    best_for: 'Seeing the reasoning as a path of questions, and what you can start today in parallel.'
  }
];

const ALGORITHM_ICONS = {
  mcda: <Scale className="w-4 h-4 text-[#cc785c]" />,
  decision_tree: <GitBranch className="w-4 h-4 text-[#cc785c]" />,
  topological: <Layers className="w-4 h-4 text-[#cc785c]" />,
  bfs: <Network className="w-4 h-4 text-[#cc785c]" />
};

const PIPELINE = [
  {
    number: '01',
    title: 'Describe what you can do',
    desc: 'Pick your degree, the skills you already have and the work that genuinely interests you. Short forms like "js" or "ml" are understood.',
    icon: <Target className="w-5 h-5 text-[#cc785c]" />
  },
  {
    number: '02',
    title: 'Weighted scoring across every track',
    desc: 'Each career is scored on 50% skills, 30% interests and 20% education, with must-have skills counted double so a critical gap actually shows.',
    icon: <Sliders className="w-5 h-5 text-[#cc785c]" />
  },
  {
    number: '03',
    title: 'Prerequisite graph traversal',
    desc: 'Your gaps are closed over a dependency graph, so JavaScript is never scheduled after React and missing prerequisites are pulled in automatically.',
    icon: <GitBranch className="w-5 h-5 text-[#cc785c]" />
  },
  {
    number: '04',
    title: 'A dated career path, not a list',
    desc: 'Skills are grouped into phases with week ranges from your study pace, then mapped onto a five-stage role ladder with salary bands.',
    icon: <Route className="w-5 h-5 text-[#cc785c]" />
  }
];

export default function Home({ onGetStarted }) {
  const [stats, setStats] = useState(FALLBACK_STATS);
  const [topSkills, setTopSkills] = useState([]);
  const [careers, setCareers] = useState([]);
  const [algorithmCatalog, setAlgorithmCatalog] = useState(null);
  const [activeCategory, setActiveCategory] = useState('All');
  const [query, setQuery] = useState('');

  useEffect(() => {
    let isMounted = true;

    fetchKnowledgeBaseStats()
      .then((data) => {
        if (!isMounted) return;
        if (data?.knowledge_base) setStats(data.knowledge_base);
        if (data?.most_in_demand_skills) setTopSkills(data.most_in_demand_skills.slice(0, 10));
      })
      .catch((err) => console.warn('Stats unavailable, using fallback counters:', err.message));

    fetchCareersCatalog({ view: 'summary' })
      .then((data) => {
        if (isMounted && data?.careers) setCareers(data.careers);
      })
      .catch((err) => console.warn('Career catalog unavailable:', err.message));

    fetchAlgorithmCatalog()
      .then((data) => {
        if (isMounted && data) setAlgorithmCatalog(data);
      })
      .catch((err) => console.warn('Algorithm catalog unavailable:', err.message));

    return () => { isMounted = false; };
  }, []);

  const categories = useMemo(
    () => ['All', ...Array.from(new Set(careers.map((c) => c.category))).sort()],
    [careers]
  );

  const visibleCareers = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return careers.filter((career) => {
      const matchesCategory = activeCategory === 'All' || career.category === activeCategory;
      const matchesQuery =
        !needle ||
        career.title.toLowerCase().includes(needle) ||
        career.required_skills.some((skill) => skill.toLowerCase().includes(needle));
      return matchesCategory && matchesQuery;
    });
  }, [careers, activeCategory, query]);

  const combos = algorithmCatalog?.combos?.length ? algorithmCatalog.combos : FALLBACK_COMBOS;

  const findAlgorithm = (family, id) =>
    (algorithmCatalog?.[family] || []).find((entry) => entry.id === id) || null;

  const counters = [
    { value: stats.total_careers, label: 'Career tracks' },
    { value: stats.total_skills, label: 'Skills mapped' },
    { value: stats.total_career_stages, label: 'Role stages' },
    { value: stats.total_roadmap_steps, label: 'Roadmap steps' }
  ];

  return (
    <div className="space-y-20 py-10 sm:py-16">

      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto px-4 space-y-6">

        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium bg-[#efe9de] text-[#141413] border border-[#e6dfd8] shadow-2xs">
          <Sparkles className="w-3.5 h-3.5 text-[#cc785c]" />
          <span>Explainable Rule-Based Career Intelligence</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-editorial font-normal text-[#141413] tracking-tight leading-[1.08] max-w-3xl mx-auto">
          Get a career path with <span className="text-[#cc785c] italic">dates on it,</span> not just advice.
        </h1>

        <p className="text-base sm:text-lg text-[#6c6a64] max-w-2xl mx-auto leading-relaxed">
          Tell the system what you already know. It scores you against every career track, finds the
          exact gaps, orders them by what depends on what, and turns them into phased weeks you can
          actually start on Monday.
        </p>

        <div className="pt-3 flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={onGetStarted}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3 rounded-lg font-medium text-sm text-white bg-[#cc785c] hover:bg-[#a9583e] active:bg-[#8f4730] transition-colors shadow-xs cursor-pointer"
          >
            <span>Generate My Career Path</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Live knowledge base counters */}
        <div className="pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-2xl mx-auto">
          {counters.map((counter) => (
            <div
              key={counter.label}
              className="bg-white border border-[#e6dfd8] rounded-xl px-3 py-4 shadow-2xs"
            >
              <div className="text-2xl sm:text-3xl font-editorial text-[#141413] leading-none">
                {counter.value}
              </div>
              <div className="text-[11px] font-semibold uppercase tracking-wider text-[#8e8b82] mt-1.5">
                {counter.label}
              </div>
            </div>
          ))}
        </div>

        <div className="pt-2 flex flex-wrap items-center justify-center gap-5 text-xs text-[#8e8b82]">
          <span className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
            50% skills - 30% interests - 20% education
          </span>
          <span className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
            No trained model, no API keys
          </span>
          <span className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
            Same input, same output - every time
          </span>
        </div>

      </section>

      {/* 4-Step Pipeline */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-10 space-y-2">
          <h2 className="text-3xl font-editorial font-normal text-[#141413]">
            How your path gets generated
          </h2>
          <p className="text-xs text-[#6c6a64] max-w-lg mx-auto leading-relaxed">
            Four deterministic stages. Every number the dashboard shows you can be traced back to a
            rule in the knowledge base.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {PIPELINE.map((step) => (
            <div
              key={step.number}
              className="bg-[#efe9de] p-6 rounded-xl border border-[#e6dfd8] space-y-3.5 relative overflow-hidden"
            >
              <div className="text-3xl font-editorial text-[#d6cbbe] absolute top-4 right-5 select-none font-normal">
                {step.number}
              </div>
              <div className="w-10 h-10 rounded-lg bg-[#faf9f5] flex items-center justify-center border border-[#e6dfd8]">
                {step.icon}
              </div>
              <div>
                <h3 className="text-base font-editorial font-normal text-[#141413] mb-1.5 leading-snug">
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

      {/* The two algorithm combinations */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-10 space-y-2">
          <h2 className="text-3xl font-editorial font-normal text-[#141413]">
            Two algorithm combinations, your choice
          </h2>
          <p className="text-xs text-[#6c6a64] max-w-xl mx-auto leading-relaxed">
            The same profile and the same knowledge base, reasoned over in two different ways. Each
            pairs a method for ranking careers with a method for ordering the learning path, and you
            can switch between them on the dashboard and compare the results side by side.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {combos.map((combo) => {
            const scoring = findAlgorithm('scoring_algorithms', combo.scoring);
            const path = findAlgorithm('path_algorithms', combo.path);

            return (
              <div
                key={combo.id}
                className="bg-white border border-[#e6dfd8] rounded-xl p-6 shadow-2xs space-y-4"
              >
                <div className="flex items-start gap-3">
                  <span className="w-8 h-8 rounded-lg bg-[#efe9de] border border-[#e6dfd8] text-[#cc785c] font-mono text-xs font-bold flex items-center justify-center shrink-0">
                    {combo.label.replace('Combo ', '')}
                  </span>
                  <div>
                    <h3 className="text-lg font-editorial font-normal text-[#141413] leading-snug">
                      {combo.label}
                    </h3>
                    <p className="text-xs text-[#6c6a64] mt-0.5">{combo.tagline}</p>
                  </div>
                </div>

                <div className="space-y-3 bg-[#faf9f5] border border-[#e6dfd8] rounded-lg p-4">
                  <div className="flex items-start gap-2.5">
                    <span className="w-7 h-7 rounded-lg bg-white border border-[#e6dfd8] flex items-center justify-center shrink-0">
                      {ALGORITHM_ICONS[combo.scoring] || <Cpu className="w-4 h-4 text-[#cc785c]" />}
                    </span>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold text-[#141413]">
                        {scoring?.name || combo.scoring}
                      </div>
                      <p className="text-[11px] text-[#6c6a64] leading-relaxed mt-0.5">
                        {scoring?.one_line}
                      </p>
                      <p className="text-[10px] font-mono text-[#8e8b82] mt-1">
                        ranks the careers
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 pl-1">
                    <Plus className="w-3 h-3 text-[#8e8b82]" />
                    <span className="h-px flex-1 bg-[#e6dfd8]" />
                  </div>

                  <div className="flex items-start gap-2.5">
                    <span className="w-7 h-7 rounded-lg bg-white border border-[#e6dfd8] flex items-center justify-center shrink-0">
                      {ALGORITHM_ICONS[combo.path] || <Route className="w-4 h-4 text-[#cc785c]" />}
                    </span>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold text-[#141413]">
                        {path?.name || combo.path}
                      </div>
                      <p className="text-[11px] text-[#6c6a64] leading-relaxed mt-0.5">
                        {path?.one_line}
                      </p>
                      <p className="text-[10px] font-mono text-[#8e8b82] mt-1">
                        orders the learning path
                      </p>
                    </div>
                  </div>
                </div>

                <p className="text-xs text-[#55534e] leading-relaxed">
                  <span className="font-semibold text-[#141413]">Best for: </span>
                  {combo.best_for}
                </p>
              </div>
            );
          })}
        </div>

        <p className="text-[11px] text-[#8e8b82] text-center mt-5 leading-relaxed">
          Both are deterministic and rule-based: the same input always produces the same output, and
          every number can be traced back to a rule. Nothing is trained, and no external AI service is called.
        </p>
      </section>

      {/* What you actually get */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {[
            {
              icon: <CalendarClock className="w-5 h-5 text-[#cc785c]" />,
              title: 'A phased timeline',
              desc: 'Foundations, core role skills, specialisation and portfolio work - each with week ranges computed from the hours you can genuinely study.'
            },
            {
              icon: <TrendingUp className="w-5 h-5 text-[#cc785c]" />,
              title: 'Where the career goes',
              desc: 'A five-stage ladder per track, from the entry role to architect or head of function, with experience ranges and indicative Indian salary bands.'
            },
            {
              icon: <Cpu className="w-5 h-5 text-[#cc785c]" />,
              title: 'Reasons, not a black box',
              desc: 'Every score shows its skill, interest and education components, which skills were credited as prerequisites, and why each gap was sequenced where it is.'
            }
          ].map((item) => (
            <div key={item.title} className="bg-white border border-[#e6dfd8] rounded-xl p-6 space-y-3 shadow-2xs">
              <div className="w-10 h-10 rounded-lg bg-[#efe9de] flex items-center justify-center border border-[#e6dfd8]">
                {item.icon}
              </div>
              <h3 className="text-lg font-editorial font-normal text-[#141413]">{item.title}</h3>
              <p className="text-xs text-[#6c6a64] leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Most in-demand skills, straight from the knowledge base */}
      {topSkills.length > 0 && (
        <section className="max-w-6xl mx-auto px-4">
          <div className="bg-white border border-[#e6dfd8] rounded-2xl p-6 sm:p-8 shadow-2xs space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
              <div className="space-y-1.5">
                <span className="text-[11px] font-mono text-[#cc785c] uppercase tracking-wider flex items-center gap-1.5">
                  <Flame className="w-3.5 h-3.5" />
                  Highest leverage skills
                </span>
                <h3 className="text-2xl font-editorial font-normal text-[#141413]">
                  Learn these and many doors open at once
                </h3>
                <p className="text-xs text-[#6c6a64] leading-relaxed max-w-xl">
                  Counted directly from how many of the {stats.total_careers} tracks require each skill - useful when you
                  have not picked a direction yet.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {topSkills.map((item) => (
                <div
                  key={item.skill}
                  className="flex items-center gap-3 bg-[#faf9f5] border border-[#e6dfd8] rounded-lg px-3 py-2.5"
                >
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-semibold text-[#141413] truncate">{item.skill}</div>
                    <div className="text-[10px] text-[#8e8b82] font-mono">
                      {item.difficulty} - about {item.learning_hours} hrs
                    </div>
                  </div>
                  <div className="shrink-0 w-28">
                    <div className="w-full bg-[#efe9de] h-1.5 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-[#cc785c] rounded-full"
                        style={{ width: `${(item.required_by / stats.total_careers) * 100}%` }}
                      />
                    </div>
                    <div className="text-[10px] font-mono text-[#8e8b82] mt-1 text-right">
                      {item.required_by} / {stats.total_careers} roles
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Career catalog (Dark Product Chrome) */}
      <section className="max-w-6xl mx-auto px-4 pb-4">
        <div className="bg-[#2e2a26] text-[#faf9f5] rounded-2xl p-6 sm:p-10 border border-[#4a443d] shadow-sm">

          <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-5 mb-7">
            <div className="max-w-xl space-y-1.5">
              <span className="text-[11px] font-mono text-[#cc785c] uppercase tracking-wider">
                Domain Competency Catalog
              </span>
              <h3 className="text-2xl font-editorial font-normal text-[#faf9f5]">
                {stats.total_careers} career tracks, each fully mapped
              </h3>
              <p className="text-xs text-[#c2bbb0] leading-relaxed">
                Every track defines its benchmark skills, must-have subset, accepted degrees, entry salary
                band and a five-stage role ladder.
              </p>
            </div>

            <div className="relative w-full lg:w-72">
              <Search className="w-4 h-4 text-[#8e8b82] absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search a career or skill..."
                className="w-full pl-9 pr-3 py-2.5 rounded-lg border border-[#4a443d] bg-[#3a3530] text-xs text-[#faf9f5] placeholder:text-[#6c6a64] focus:outline-hidden focus:border-[#cc785c] transition-colors"
              />
            </div>
          </div>

          {/* Category filter */}
          {categories.length > 1 && (
            <div className="flex flex-wrap gap-1.5 mb-5">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setActiveCategory(category)}
                  className={`px-2.5 py-1 rounded-md text-[11px] font-medium border transition-colors cursor-pointer ${
                    activeCategory === category
                      ? 'bg-[#cc785c] text-white border-[#cc785c]'
                      : 'bg-[#3a3530] text-[#c2bbb0] border-[#4a443d] hover:border-[#5d554b] hover:text-[#faf9f5]'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {visibleCareers.map((career) => (
              <div
                key={career.id}
                className="bg-[#3a3530] border border-[#4a443d] p-4 rounded-xl hover:border-[#5d554b] transition-colors flex flex-col gap-2.5"
              >
                <div className="flex items-start justify-between gap-2">
                  <h4 className="font-medium text-sm text-[#faf9f5] leading-snug">
                    {career.title}
                  </h4>
                  {career.demand && (
                    <span className="text-[10px] font-mono text-[#cc785c] shrink-0 mt-0.5">
                      {career.demand}
                    </span>
                  )}
                </div>

                <p className="text-[11px] text-[#c2bbb0] font-mono leading-relaxed">
                  {career.required_skills.slice(0, 5).join(', ')}
                  {career.required_skills.length > 5 && ` +${career.required_skills.length - 5}`}
                </p>

                <div className="mt-auto pt-2 border-t border-[#4a443d] flex items-center justify-between text-[10px] text-[#8e8b82] font-mono">
                  <span className="inline-flex items-center gap-1">
                    <IndianRupee className="w-3 h-3" />
                    {career.entry_salary_inr}
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <Layers className="w-3 h-3" />
                    {career.total_stages} stages
                  </span>
                </div>
              </div>
            ))}
          </div>

          {visibleCareers.length === 0 && careers.length > 0 && (
            <p className="text-xs text-[#c2bbb0] italic py-6 text-center">
              No track matches "{query}". Try a skill name like "python" or "figma".
            </p>
          )}

          {careers.length === 0 && (
            <p className="text-xs text-[#c2bbb0] italic py-6 text-center">
              Start the Flask backend to load the live career catalog.
            </p>
          )}

          <div className="mt-8 pt-6 border-t border-[#4a443d] flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-xs text-[#c2bbb0]">
              Ready to see which of these {stats.total_careers} tracks fits you, and exactly how to get there?
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
