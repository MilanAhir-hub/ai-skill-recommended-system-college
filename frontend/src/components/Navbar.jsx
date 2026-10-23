/**
 * components/Navbar.jsx
 * ---------------------
 * Top navigation bar aligned with Claude's editorial design system.
 * Warm cream canvas (#faf9f5), hairline divider (#e6dfd8), radial spike mark,
 * and pill tabs.
 */

import React, { useState, useEffect } from 'react';
import { Sparkles, Menu, X, ArrowUpRight } from 'lucide-react';
import { checkApiHealth } from '../services/api';

export default function Navbar({ activePage, setActivePage, currentUserId }) {
  const [backendOnline, setBackendOnline] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Check backend health on mount
  useEffect(() => {
    let isMounted = true;
    checkApiHealth()
      .then(() => {
        if (isMounted) setBackendOnline(true);
      })
      .catch(() => {
        if (isMounted) setBackendOnline(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleNavClick = (page) => {
    setActivePage(page);
    setMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 bg-[#faf9f5]/90 backdrop-blur-md border-b border-[#e6dfd8]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand with Anthropic-inspired radial mark */}
          <div 
            onClick={() => handleNavClick('home')}
            className="flex items-center gap-3 cursor-pointer group select-none"
          >
            {/* 4-Spoke Radial Spike Mark */}
            <div className="w-8 h-8 rounded-lg bg-[#141413] flex items-center justify-center text-[#faf9f5] group-hover:scale-105 transition-transform shadow-xs">
              <svg 
                viewBox="0 0 24 24" 
                fill="currentColor" 
                className="w-4 h-4 text-[#cc785c]"
              >
                <path d="M12 2L13.8 8.8L20.6 7L15.8 12L20.6 17L13.8 15.2L12 22L10.2 15.2L3.4 17L8.2 12L3.4 7L10.2 8.8L12 2Z" />
              </svg>
            </div>
            
            <div className="flex items-baseline gap-1.5">
              <span className="text-lg font-bold tracking-tight text-[#141413]">
                CareerCompass
              </span>
              <span className="text-xs font-semibold uppercase tracking-wider text-[#cc785c] px-1.5 py-0.5 rounded-full bg-[#f5f0e8] border border-[#e6dfd8]">
                AI
              </span>
            </div>
          </div>

          {/* Desktop Navigation Tabs */}
          <nav className="hidden md:flex items-center gap-1.5">
            <button
              onClick={() => handleNavClick('home')}
              className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
                activePage === 'home'
                  ? 'bg-[#efe9de] text-[#141413] shadow-2xs font-semibold'
                  : 'text-[#6c6a64] hover:text-[#141413] hover:bg-[#f5f0e8]'
              }`}
            >
              Overview
            </button>

            <button
              onClick={() => handleNavClick('profile')}
              className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
                activePage === 'profile'
                  ? 'bg-[#efe9de] text-[#141413] shadow-2xs font-semibold'
                  : 'text-[#6c6a64] hover:text-[#141413] hover:bg-[#f5f0e8]'
              }`}
            >
              Student Profile
            </button>

            <button
              onClick={() => handleNavClick('dashboard')}
              className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
                activePage === 'dashboard'
                  ? 'bg-[#efe9de] text-[#141413] shadow-2xs font-semibold'
                  : 'text-[#6c6a64] hover:text-[#141413] hover:bg-[#f5f0e8]'
              } ${!currentUserId ? 'opacity-60' : ''}`}
            >
              Recommendations
              {currentUserId && (
                <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-[#cc785c] text-white">
                  Active
                </span>
              )}
            </button>
          </nav>

          {/* Right Action Cluster: Status Badge & Primary CTA */}
          <div className="flex items-center gap-3">
            
            {/* Backend Health Status Pill */}
            <div
              className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border ${
                backendOnline === true
                  ? 'bg-[#f5f0e8] text-[#252523] border-[#e6dfd8]'
                  : backendOnline === false
                  ? 'bg-rose-50 text-rose-800 border-rose-200'
                  : 'bg-[#f5f0e8] text-[#6c6a64] border-[#e6dfd8]'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  backendOnline === true
                    ? 'bg-[#5db872] ring-2 ring-[#5db872]/20 animate-pulse'
                    : backendOnline === false
                    ? 'bg-[#c64545]'
                    : 'bg-[#8e8b82]'
                }`}
              />
              <span className="hidden sm:inline font-mono text-[11px]">
                {backendOnline === true
                  ? 'Engine Online'
                  : backendOnline === false
                  ? 'Engine Offline'
                  : 'Connecting...'}
              </span>
            </div>

            {/* Quick Action Button */}
            <button
              onClick={() => handleNavClick('profile')}
              className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] active:bg-[#8f4730] transition-colors shadow-xs cursor-pointer"
            >
              <span>Get Evaluated</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-[#3d3d3a] hover:text-[#141413] hover:bg-[#f5f0e8] rounded-lg cursor-pointer"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-[#e6dfd8] bg-[#faf9f5] px-4 pt-3 pb-5 space-y-1.5">
          <button
            onClick={() => handleNavClick('home')}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium ${
              activePage === 'home' ? 'bg-[#efe9de] text-[#141413] font-semibold' : 'text-[#3d3d3a] hover:bg-[#f5f0e8]'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => handleNavClick('profile')}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium ${
              activePage === 'profile' ? 'bg-[#efe9de] text-[#141413] font-semibold' : 'text-[#3d3d3a] hover:bg-[#f5f0e8]'
            }`}
          >
            Student Profile
          </button>
          <button
            onClick={() => handleNavClick('dashboard')}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium ${
              activePage === 'dashboard' ? 'bg-[#efe9de] text-[#141413] font-semibold' : 'text-[#3d3d3a] hover:bg-[#f5f0e8]'
            }`}
          >
            Recommendations {currentUserId ? '(Active)' : ''}
          </button>
        </div>
      )}
    </header>
  );
}
