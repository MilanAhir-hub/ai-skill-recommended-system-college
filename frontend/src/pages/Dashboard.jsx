/**
 * pages/Dashboard.jsx
 * -------------------
 * Career recommendation dashboard styled with Claude's warm editorial principles.
 * Shows the student profile summary, the explainable scoring + career path
 * algorithm, ranked career cards with generated paths, and an explorer that
 * can generate the path for any career in the knowledge base.
 */

import React, { useState, useEffect } from 'react';
import {
  RotateCcw,
  UserPlus,
  ArrowLeft,
  AlertCircle,
  GraduationCap,
  Target,
  Check,
  Sliders,
  Sparkles,
  Cpu,
  Clock,
  ListOrdered,
  Compass,
  Loader2,
  X,
  Route
} from 'lucide-react';
import { fetchRecommendations, fetchCareersCatalog, fetchCareerPath } from '../services/api';
import CareerCard from '../components/CareerCard';
import CareerPath from '../components/CareerPath';
import Loading from '../components/Loading';

const DEFAULT_AI_ALGO = {
  name: "Rule-Based Expert System (Weighted MCDA + Prerequisite Graph)",
  short_name: "Rule-Based Expert System & MCDA",
  description: "An explainable heuristic algorithm that scores competencies, interests and academic background to rank career pathways, then traverses a skill prerequisite graph to generate an ordered, time-estimated career path. Fully deterministic: no trained model and no external AI service is used.",
  steps: [
    {
      title: "Profile Normalization",
      desc: "Standardized entered skills through alias matching into canonical knowledge-base tokens."
    },
    {
      title: "Weighted Skill Gap Analysis (50%)",
      desc: "Compared your skills against each career's benchmark set, counting must-have core skills double."
    },
    {
      title: "Interest Alignment (30%)",
      desc: "Measured overlap between your selected interests and each career's day-to-day domain focus."
    },
    {
      title: "Education Compatibility (20%)",
      desc: "Matched your degree against each career's accepted academic keywords, with a partial-credit fallback."
    },
    {
      title: "Score Prediction & Ranking",
      desc: "Aggregated the weighted factors (plus a goal bonus) into a 0-100 fit score and ranked every career."
    },
    {
      title: "Prerequisite Graph Traversal",
      desc: "Pulled in missing prerequisites as bridge skills, then topologically ordered every skill you need."
    },
    {
      title: "Career Path Generation",
      desc: "Grouped the ordered skills into phases, estimated weeks from your study pace, and attached the role ladder."
    }
  ]
};

const PACE_OPTIONS = [
  { value: 5, label: '5 hrs / week (light)' },
  { value: 10, label: '10 hrs / week (balanced)' },
  { value: 15, label: '15 hrs / week (focused)' },
  { value: 20, label: '20 hrs / week (intensive)' },
  { value: 30, label: '30 hrs / week (full-time prep)' }
];

const COUNT_OPTIONS = [3, 5, 8];

export default function Dashboard({
  userId,
  userProfile,
  onCreateNewProfile,
  onGoHome
}) {
  const [recommendations, setRecommendations] = useState([]);
  const [aiAlgoInfo, setAiAlgoInfo] = useState(DEFAULT_AI_ALGO);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [metaInfo, setMetaInfo] = useState(null);

  const [hoursPerWeek, setHoursPerWeek] = useState(userProfile?.hours_per_week || 10);
  const [topN, setTopN] = useState(3);

  // Career explorer state
  const [catalog, setCatalog] = useState([]);
  const [exploreId, setExploreId] = useState('');
  const [exploreResult, setExploreResult] = useState(null);
  const [exploreLoading, setExploreLoading] = useState(false);
  const [exploreError, setExploreError] = useState('');

  const loadRecommendations = async (options = {}) => {
    if (!userId) {
      setLoading(false);
      return;
    }

    const pace = options.hoursPerWeek ?? hoursPerWeek;
    const count = options.topN ?? topN;

    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetchRecommendations(userId, {
        hours_per_week: pace,
        top_n: count
      });
      setRecommendations(response.recommendations || []);
      setAiAlgoInfo(response.ai_algo || DEFAULT_AI_ALGO);
      setMetaInfo({
        userName: response.user_name || userProfile?.name || 'Student',
        education: response.user_education || userProfile?.education || '',
        goal: response.user_goal || userProfile?.career_goal || '',
        total: response.total_recommendations || 0,
        evaluated: response.careers_evaluated || 0,
        pace: response.hours_per_week || pace
      });
    } catch (err) {
      setErrorMessage(
        err.message || 'Unable to retrieve career recommendations. Please verify the Flask server is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecommendations();
  }, [userId]);

  // Load the career catalog once so the explorer can offer every career
  useEffect(() => {
    let isMounted = true;
    fetchCareersCatalog({ view: 'summary' })
      .then((data) => {
        if (isMounted && data?.careers) setCatalog(data.careers);
      })
      .catch(() => {
        /* Explorer is optional; silently skip when the catalog is unavailable */
      });
    return () => { isMounted = false; };
  }, []);

  const handlePaceChange = (value) => {
    const pace = parseInt(value, 10);
    setHoursPerWeek(pace);
    loadRecommendations({ hoursPerWeek: pace });
    if (exploreResult) handleExplore(exploreResult.career_id, pace);
  };

  const handleCountChange = (value) => {
    const count = parseInt(value, 10);
    setTopN(count);
    loadRecommendations({ topN: count });
  };

  const handleExplore = async (careerId, pace = hoursPerWeek) => {
    if (!careerId || !userId) return;

    setExploreId(careerId);
    setExploreLoading(true);
    setExploreError('');

    try {
      const response = await fetchCareerPath(userId, careerId, { hours_per_week: pace });
      setExploreResult(response.evaluation);
    } catch (err) {
      setExploreError(err.message || 'Failed to generate that career path.');
      setExploreResult(null);
    } finally {
      setExploreLoading(false);
    }
  };

  // 1. Empty State
  if (!userId) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center">
        <div className="w-14 h-14 rounded-2xl bg-[#efe9de] text-[#cc785c] flex items-center justify-center mx-auto mb-4 border border-[#e6dfd8]">
          <AlertCircle className="w-7 h-7" />
        </div>
        <h2 className="text-2xl font-editorial font-normal text-[#141413] mb-2">
          No Profile Selected
        </h2>
        <p className="text-xs text-[#6c6a64] mb-6 max-w-sm mx-auto leading-relaxed">
          Please complete your student profile so our rule-based engine can compute
          match scores, identify skill gaps and generate your career path.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={onCreateNewProfile}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] transition-colors shadow-xs cursor-pointer"
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Create Profile</span>
          </button>
          <button
            onClick={onGoHome}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg text-xs font-semibold text-[#141413] bg-[#faf9f5] border border-[#e6dfd8] hover:bg-[#f5f0e8] transition-colors cursor-pointer"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Overview</span>
          </button>
        </div>
      </div>
    );
  }

  // 2. Loading State
  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16">
        <Loading message="Scoring your profile against every career track, then traversing the skill prerequisite graph to build your career path..." />
      </div>
    );
  }

  // 3. Error State
  if (errorMessage) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center">
        <div className="w-14 h-14 rounded-2xl bg-rose-50 text-[#c64545] flex items-center justify-center mx-auto mb-4 border border-rose-200">
          <AlertCircle className="w-7 h-7" />
        </div>
        <h2 className="text-2xl font-editorial font-normal text-[#141413] mb-2">
          Unable to Load Recommendations
        </h2>
        <p className="text-xs text-[#6c6a64] mb-6 max-w-sm mx-auto leading-relaxed">
          {errorMessage}
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={() => loadRecommendations()}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] transition-colors shadow-xs cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Retry Evaluation</span>
          </button>
          <button
            onClick={onCreateNewProfile}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg text-xs font-semibold text-[#141413] bg-[#faf9f5] border border-[#e6dfd8] hover:bg-[#f5f0e8] transition-colors cursor-pointer"
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Edit Profile</span>
          </button>
        </div>
      </div>
    );
  }

  const exploreOptions = catalog.filter(
    (career) => !recommendations.some((rec) => rec.career_id === career.id)
  );

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 sm:py-12 space-y-8">

      {/* Profile Overview Banner (Warm Cream Card) */}
      <div className="bg-white p-6 sm:p-8 rounded-xl border border-[#e6dfd8] shadow-2xs">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">

          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[#f5f0e8] text-[#141413] border border-[#e6dfd8]">
              <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
              <span>
                {metaInfo?.evaluated
                  ? `${metaInfo.evaluated} careers evaluated - top ${metaInfo.total} shown`
                  : `Evaluation complete - top ${metaInfo?.total || 0}`}
              </span>
            </div>

            <h1 className="text-3xl sm:text-4xl font-editorial font-normal text-[#141413] tracking-tight">
              Career paths for <span className="italic text-[#cc785c]">{metaInfo?.userName || 'You'}</span>
            </h1>

            <div className="flex flex-wrap items-center gap-3 text-xs text-[#6c6a64] pt-1">
              {metaInfo?.education && (
                <span className="flex items-center gap-1.5 bg-[#faf9f5] px-2.5 py-1 rounded-md border border-[#e6dfd8]">
                  <GraduationCap className="w-3.5 h-3.5 text-[#8e8b82]" />
                  {metaInfo.education}
                </span>
              )}
              {metaInfo?.goal && (
                <span className="flex items-center gap-1.5 bg-[#f5f0e8] text-[#cc785c] px-2.5 py-1 rounded-md border border-[#e6dfd8] font-medium">
                  <Target className="w-3.5 h-3.5" />
                  Target: {metaInfo.goal}
                </span>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => loadRecommendations()}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-medium text-[#141413] bg-[#faf9f5] border border-[#e6dfd8] hover:bg-[#f5f0e8] transition-colors cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5 text-[#8e8b82]" />
              <span>Refresh</span>
            </button>
            <button
              onClick={onCreateNewProfile}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] transition-colors shadow-xs cursor-pointer"
            >
              <UserPlus className="w-3.5 h-3.5" />
              <span>Evaluate Another Profile</span>
            </button>
          </div>

        </div>

        {/* Path controls: study pace + how many careers to show */}
        <div className="mt-6 pt-5 border-t border-[#e6dfd8] flex flex-col lg:flex-row lg:items-end gap-4">
          <div className="flex-1 space-y-1.5">
            <label className="text-[11px] font-semibold uppercase tracking-wider text-[#141413] flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-[#cc785c]" />
              Study pace (drives every timeline below)
            </label>
            <select
              value={hoursPerWeek}
              onChange={(e) => handlePaceChange(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-[#e6dfd8] text-xs text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all cursor-pointer"
            >
              {PACE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>

          <div className="w-full lg:w-56 space-y-1.5">
            <label className="text-[11px] font-semibold uppercase tracking-wider text-[#141413] flex items-center gap-1.5">
              <ListOrdered className="w-3.5 h-3.5 text-[#cc785c]" />
              Careers to show
            </label>
            <select
              value={topN}
              onChange={(e) => handleCountChange(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-[#e6dfd8] text-xs text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all cursor-pointer"
            >
              {COUNT_OPTIONS.map((count) => (
                <option key={count} value={count}>Top {count} matches</option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-[#8e8b82]">
          <div className="flex items-center gap-2">
            <Sliders className="w-3.5 h-3.5 text-[#cc785c] shrink-0" />
            <span>
              Heuristic weights: <strong className="text-[#141413]">50% skills</strong> + <strong className="text-[#141413]">30% interests</strong> + <strong className="text-[#141413]">20% education</strong>, must-have skills counted double
            </span>
          </div>
          <span className="font-mono text-[11px] text-[#8e8b82]">
            Deterministic rule-based engine
          </span>
        </div>
      </div>

      {/* AI Algo Explanation Section */}
      <div className="bg-white rounded-xl border border-[#e6dfd8] p-6 sm:p-8 shadow-2xs space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#e6dfd8]">
          <div className="flex items-start sm:items-center gap-3.5">
            <div className="w-11 h-11 rounded-xl bg-[#efe9de] text-[#cc785c] flex items-center justify-center shrink-0 border border-[#e6dfd8] mt-0.5 sm:mt-0">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="inline-flex items-center gap-1 text-xs font-bold uppercase tracking-wider text-[#cc785c] bg-[#f5f0e8] px-2.5 py-1 rounded-md border border-[#e6dfd8]">
                  AI Algo:-
                </span>
                <h2 className="text-xl sm:text-2xl font-editorial font-normal text-[#141413]">
                  {aiAlgoInfo?.name || DEFAULT_AI_ALGO.name}
                </h2>
              </div>
              <p className="text-xs text-[#6c6a64] mt-1 leading-relaxed">
                {aiAlgoInfo?.description || DEFAULT_AI_ALGO.description}
              </p>
            </div>
          </div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-medium bg-[#faf9f5] text-[#8e8b82] border border-[#e6dfd8] shrink-0 self-start sm:self-auto">
            <Sparkles className="w-3.5 h-3.5 text-[#cc785c]" />
            Explainable AI
          </span>
        </div>

        <div className="space-y-3">
          <p className="text-xs font-semibold text-[#141413] flex items-center gap-1.5">
            <Sliders className="w-3.5 h-3.5 text-[#cc785c]" />
            How the algorithm scored your profile and generated each career path:
          </p>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-0.5">
            {(aiAlgoInfo?.steps || DEFAULT_AI_ALGO.steps).map((step, idx) => (
              <li
                key={idx}
                className="flex items-start gap-3 p-3.5 rounded-lg bg-[#faf9f5] border border-[#e6dfd8]/80 hover:border-[#cc785c]/40 transition-colors"
              >
                <span className="w-5 h-5 rounded-full bg-[#efe9de] text-[#cc785c] font-mono text-[11px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {idx + 1}
                </span>
                <div className="text-xs leading-relaxed text-[#3d3d3a]">
                  <strong className="text-[#141413] font-semibold">{step.title}: </strong>
                  <span>{step.desc}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Ranked Career Cards */}
      {recommendations.length > 0 ? (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-editorial font-normal text-[#141413] flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-[#cc785c]" />
              Ranked Career Matches
            </h2>
            <span className="text-xs font-mono text-[#8e8b82]">
              Top {recommendations.length} of {metaInfo?.evaluated || recommendations.length}
            </span>
          </div>

          <div className="space-y-6">
            {recommendations.map((career, index) => (
              <CareerCard
                key={career.career_id || index}
                career={career}
                rank={index + 1}
              />
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-xl border border-[#e6dfd8] p-8">
          <p className="text-xs text-[#6c6a64]">
            No recommendations generated. Please update your profile with additional skills or interests.
          </p>
          <button
            onClick={onCreateNewProfile}
            className="mt-4 px-5 py-2 rounded-lg bg-[#cc785c] text-white text-xs font-medium cursor-pointer"
          >
            Update Profile
          </button>
        </div>
      )}

      {/* Explore any other career path */}
      {exploreOptions.length > 0 && (
        <div className="bg-white rounded-xl border border-[#e6dfd8] p-6 sm:p-8 shadow-2xs space-y-5">
          <div className="space-y-1.5">
            <h2 className="text-2xl font-editorial font-normal text-[#141413] flex items-center gap-2">
              <Compass className="w-5 h-5 text-[#cc785c]" />
              Explore Any Other Career
            </h2>
            <p className="text-xs text-[#6c6a64] leading-relaxed max-w-2xl">
              Not convinced by your top matches? Generate the full path - gaps, phases, timeline and role
              ladder - for any career in the knowledge base, scored against the same profile.
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            {exploreOptions.map((career) => (
              <button
                key={career.id}
                onClick={() => handleExplore(career.id)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                  exploreId === career.id
                    ? 'bg-[#141413] text-[#faf9f5] border-[#141413]'
                    : 'bg-[#faf9f5] text-[#3d3d3a] border-[#e6dfd8] hover:border-[#cc785c]/60 hover:bg-[#f5f0e8]'
                }`}
              >
                {exploreId === career.id && exploreLoading
                  ? <Loader2 className="w-3 h-3 animate-spin" />
                  : <Route className="w-3 h-3 text-[#cc785c]" />}
                <span>{career.title}</span>
              </button>
            ))}
          </div>

          {exploreError && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{exploreError}</span>
            </div>
          )}

          {exploreResult && !exploreLoading && (
            <div className="pt-5 border-t border-[#e6dfd8] space-y-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h3 className="text-xl font-editorial text-[#141413]">
                    {exploreResult.career_title}
                  </h3>
                  <p className="text-xs text-[#6c6a64] mt-1 max-w-2xl leading-relaxed">
                    {exploreResult.description}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-2xl font-editorial text-[#141413] leading-none">
                      {exploreResult.matching_score}%
                    </div>
                    <div className="text-[10px] font-semibold text-[#8e8b82] uppercase tracking-wider">
                      Fit score
                    </div>
                  </div>
                  <button
                    onClick={() => { setExploreResult(null); setExploreId(''); }}
                    className="p-1.5 rounded-md text-[#8e8b82] hover:bg-[#f5f0e8] hover:text-[#141413] transition-colors cursor-pointer"
                    aria-label="Close career path"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <CareerPath careerPath={exploreResult.career_path} />
            </div>
          )}
        </div>
      )}

    </div>
  );
}
