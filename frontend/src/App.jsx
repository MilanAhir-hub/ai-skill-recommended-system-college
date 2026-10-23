/**
 * App.jsx
 * -------
 * Main entry point and page router for CareerCompass AI.
 * Styled with Claude's warm editorial design language:
 * Cream canvas (#faf9f5), Newsreader serif typography, coral CTAs (#cc785c),
 * and dark navy grounding footer (#181715).
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

      {/* Dark Footer from DESIGN.md (#181715) */}
      <footer className="border-t border-[#252320] bg-[#181715] text-[#a09d96] py-12 mt-16 text-xs">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-2.5">
              <div className="w-6 h-6 rounded-md bg-[#252320] flex items-center justify-center text-[#cc785c]">
                <svg viewBox="0 0 24 24" fill="currentColor" className="w-3.5 h-3.5">
                  <path d="M12 2L13.8 8.8L20.6 7L15.8 12L20.6 17L13.8 15.2L12 22L10.2 15.2L3.4 17L8.2 12L3.4 7L10.2 8.8L12 2Z" />
                </svg>
              </div>
              <span className="font-bold text-sm text-[#faf9f5] tracking-tight">
                CareerCompass AI
              </span>
              <span className="text-[#8e8b82] text-[11px] font-mono">
                v2.0
              </span>
            </div>

            <div className="flex items-center gap-4 text-[11px] text-[#8e8b82]">
              <button 
                onClick={() => setActivePage('home')} 
                className="hover:text-[#faf9f5] transition-colors cursor-pointer"
              >
                Overview
              </button>
              <button 
                onClick={() => setActivePage('profile')} 
                className="hover:text-[#faf9f5] transition-colors cursor-pointer"
              >
                Profile Form
              </button>
              {currentUserId && (
                <button 
                  onClick={() => setActivePage('dashboard')} 
                  className="hover:text-[#faf9f5] transition-colors cursor-pointer"
                >
                  Dashboard
                </button>
              )}
            </div>
          </div>

          <div className="pt-6 border-t border-[#252320] flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-[#6c6a64]">
            <p>
              AI-Powered Personalized Career and Skill Recommendation System • College Project
            </p>
            <p className="font-mono text-[10px]">
              Rule-Based Expert Heuristics (50% Skills • 30% Interests • 20% Education) + Prerequisite Graph Paths
            </p>
          </div>

        </div>
      </footer>

    </div>
  );
}
