/**
 * App.jsx
 * -------
 * Main entry point and page router for CareerCompass AI.
 * Styled with Claude's warm editorial design language:
 * Cream canvas (#faf9f5), Newsreader serif typography, coral CTAs (#cc785c),
 * and dark navy grounding footer (#2e2a26).
 */

import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ProfileForm from './pages/ProfileForm';
import Dashboard from './pages/Dashboard';

export default function App() {
  const [activePage, setActivePage] = useState('home');

  const [currentUserId, setCurrentUserId] = useState(() => {
    const saved = sessionStorage.getItem('career_user_id');
    return saved ? parseInt(saved, 10) : null;
  });

  const [currentUserProfile, setCurrentUserProfile] = useState(() => {
    const saved = sessionStorage.getItem('career_user_profile');
    try {
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const handleProfileCreated = (userId, profileData) => {
    setCurrentUserId(userId);
    setCurrentUserProfile(profileData);
    sessionStorage.setItem('career_user_id', userId);
    sessionStorage.setItem('career_user_profile', JSON.stringify(profileData));
    setActivePage('dashboard');
  };

  const handleCreateNewProfile = () => {
    setActivePage('profile');
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#faf9f5] text-[#3d3d3a] selection:bg-[#cc785c] selection:text-white">
      
      {/* Top Navigation Bar */}
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        currentUserId={currentUserId}
      />

      {/* Main View Area */}
      <main className="grow">
        {activePage === 'home' && (
          <Home onGetStarted={() => setActivePage('profile')} />
        )}

        {activePage === 'profile' && (
          <ProfileForm
            onProfileCreated={handleProfileCreated}
            onCancel={() => setActivePage('home')}
          />
        )}

        {activePage === 'dashboard' && (
          <Dashboard
            userId={currentUserId}
            userProfile={currentUserProfile}
            onCreateNewProfile={handleCreateNewProfile}
            onGoHome={() => setActivePage('home')}
          />
        )}
      </main>

      {/* Dark Footer from DESIGN.md (#2e2a26) */}
      <footer className="border-t border-[#4a443d] bg-[#2e2a26] text-[#c2bbb0] py-14 mt-16 text-xs">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">

          {/* Three columns: what it is, where to go, how it works */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-10">

            {/* Brand + description */}
            <div className="lg:col-span-2 space-y-3">
              <div className="flex items-baseline gap-1.5">
                <span className="text-base font-bold text-[#faf9f5] tracking-tight">
                  CareerCompass
                </span>
                <span className="text-[10px] font-semibold uppercase tracking-wider text-[#cc785c] px-1.5 py-0.5 rounded-full bg-[#4a443d] border border-[#5d554b]">
                  AI
                </span>
              </div>
              <p className="text-[11px] leading-relaxed max-w-sm text-[#c2bbb0]">
                An AI-powered personalized career and skill recommendation system. It scores your
                profile against every career track, finds the exact skill gaps, and generates a
                prerequisite-ordered learning path with real week-by-week timelines.
              </p>
              <div className="flex flex-wrap gap-x-4 gap-y-1.5 text-[10px] font-mono text-[#6c6a64] pt-1">
                <span>21 career tracks</span>
                <span>92 skills mapped</span>
                <span>105 role stages</span>
              </div>
            </div>

            {/* Navigation */}
            <div className="space-y-3">
              <h3 className="text-[10px] font-semibold uppercase tracking-wider text-[#faf9f5]">
                Navigate
              </h3>
              <ul className="space-y-2 text-[11px]">
                <li>
                  <button
                    onClick={() => setActivePage('home')}
                    className="hover:text-[#faf9f5] transition-colors cursor-pointer"
                  >
                    Overview
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setActivePage('profile')}
                    className="hover:text-[#faf9f5] transition-colors cursor-pointer"
                  >
                    Build your profile
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setActivePage('dashboard')}
                    className="hover:text-[#faf9f5] transition-colors cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                    disabled={!currentUserId}
                  >
                    Dashboard
                  </button>
                </li>
              </ul>
            </div>

            {/* The engine */}
            <div className="space-y-3">
              <h3 className="text-[10px] font-semibold uppercase tracking-wider text-[#faf9f5]">
                The engine
              </h3>
              <ul className="space-y-2.5 text-[11px]">
                <li>
                  <span className="block text-[#faf9f5]">Combo 1</span>
                  <span className="block text-[10px] font-mono text-[#6c6a64] leading-relaxed">
                    Weighted MCDA + Topological Sort
                  </span>
                </li>
                <li>
                  <span className="block text-[#faf9f5]">Combo 2</span>
                  <span className="block text-[10px] font-mono text-[#6c6a64] leading-relaxed">
                    Decision Tree + Breadth-First Search
                  </span>
                </li>
              </ul>
              <p className="text-[10px] text-[#6c6a64] leading-relaxed">
                Rule-based and deterministic. No trained model, no API keys.
              </p>
            </div>
          </div>

          {/* Team */}
          <div className="pt-8 border-t border-[#4a443d] space-y-2">
            <h3 className="text-[10px] font-semibold uppercase tracking-wider text-[#faf9f5]">
              Submitted by
            </h3>
            <div className="flex flex-wrap gap-x-5 gap-y-1.5 text-[11px] text-[#c2bbb0]">
              <span>Yash Parmar</span>
              <span>Milan Gagiya</span>
              <span>Hiren Jalondhra</span>
              <span>Vrutik Sotha</span>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="pt-6 border-t border-[#4a443d] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-[10px] text-[#6c6a64]">
            <p>
              AI-Powered Personalized Career and Skill Recommendation System &middot; College Project
            </p>
            <p className="font-mono">
              50% Skills &middot; 30% Interests &middot; 20% Education
            </p>
          </div>

        </div>
      </footer>

    </div>
  );
}
