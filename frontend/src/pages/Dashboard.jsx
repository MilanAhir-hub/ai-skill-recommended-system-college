/**
 * pages/Dashboard.jsx
 * -------------------
 * Career recommendation dashboard styled with Claude's warm editorial principles.
 * Features top student profile summary, explainable scoring callout,
 * and top 3 career cards with expandable roadmaps.
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
  Sparkles
} from 'lucide-react';
import { fetchRecommendations } from '../services/api';
import CareerCard from '../components/CareerCard';
import Loading from '../components/Loading';

export default function Dashboard({ 
  userId, 
  userProfile, 
  onCreateNewProfile, 
  onGoHome 
}) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [metaInfo, setMetaInfo] = useState(null);

  const loadRecommendations = async () => {
    if (!userId) {
      setLoading(false);
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetchRecommendations(userId);
      setRecommendations(response.recommendations || []);
      setMetaInfo({
        userName: response.user_name || userProfile?.name || 'Student',
        education: response.user_education || userProfile?.education || '',
        goal: response.user_goal || userProfile?.career_goal || '',
        total: response.total_recommendations || 0,
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
          Please complete your student profile so our heuristic AI engine can compute 
          match scores and identify skill gaps.
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
        <Loading message="Evaluating profile against heuristic career knowledge base with 50% skill, 30% interest, and 20% education weights..." />
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
            onClick={loadRecommendations}
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

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 sm:py-12 space-y-8">
      
      {/* Profile Overview Banner (Warm Cream Card) */}
      <div className="bg-white p-6 sm:p-8 rounded-xl border border-[#e6dfd8] shadow-2xs">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[#f5f0e8] text-[#141413] border border-[#e6dfd8]">
              <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5]" />
              <span>Evaluation Complete • Top 3 Recommendations</span>
            </div>
            
            <h1 className="text-3xl sm:text-4xl font-editorial font-normal text-[#141413] tracking-tight">
              Recommended Career Tracks for <span className="italic text-[#cc785c]">{metaInfo?.userName || 'You'}</span>
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
              onClick={loadRecommendations}
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

        {/* Scoring Model Note */}
        <div className="mt-6 pt-5 border-t border-[#e6dfd8] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-[#8e8b82]">
          <div className="flex items-center gap-2">
            <Sliders className="w-3.5 h-3.5 text-[#cc785c] shrink-0" />
            <span>
              Heuristic Weights: <strong className="text-[#141413]">50% Skill Match</strong> + <strong className="text-[#141413]">30% Interest Match</strong> + <strong className="text-[#141413]">20% Education Match</strong>
            </span>
          </div>
          <span className="font-mono text-[11px] text-[#8e8b82]">
            Deterministic Rule-Based Engine
          </span>
        </div>
      </div>

      {/* Top 3 Career Cards Grid */}
      {recommendations.length > 0 ? (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-editorial font-normal text-[#141413] flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-[#cc785c]" />
              Ranked Career Matches
            </h2>
            <span className="text-xs font-mono text-[#8e8b82]">
              Top {recommendations.length} Paths
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
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

    </div>
  );
}
