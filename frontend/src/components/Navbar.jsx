/**
 * components/Navbar.jsx
 * ---------------------
 * Floating glassmorphic navigation pill aligned with Claude's editorial
 * design system. It sits on the warm cream canvas (#faf9f5) as a frosted
 * rounded bar, and shrinks as the page scrolls: the pill narrows, loses
 * height, tightens its padding and deepens its shadow, all on one animated
 * transition.
 */

import React, { useState, useEffect } from 'react';
import { Menu, X, ArrowUpRight } from 'lucide-react';
import { checkApiHealth } from '../services/api';

/* Scroll distance after which the bar compacts. */
const SHRINK_AFTER = 12;

export default function Navbar({ activePage, setActivePage, currentUserId }) {
  const [backendOnline, setBackendOnline] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Initialised from the real scroll position, so a reload halfway down the
  // page renders the compact bar immediately instead of snapping into it.
  const [scrolled, setScrolled] = useState(
    () => typeof window !== 'undefined' && window.scrollY > SHRINK_AFTER
  );

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

  // Shrink on scroll
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > SHRINK_AFTER);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavClick = (page) => {
    setActivePage(page);
    setMobileMenuOpen(false);
  };

  const tabs = [
    { id: 'home', label: 'Overview' },
    { id: 'profile', label: 'Student Profile' },
    { id: 'dashboard', label: 'Recommendations' }
  ];

  const tabClass = (id) =>
    `relative rounded-full font-medium cursor-pointer transition-all duration-300 ease-out ${
      scrolled ? 'px-3 py-1 text-[13px]' : 'px-3.5 py-1.5 text-sm'
    } ${
      activePage === id
        ? 'bg-[#141413] text-[#faf9f5] shadow-xs'
        : 'text-[#6c6a64] hover:text-[#141413] hover:bg-[#f5f0e8]/80'
    } ${id === 'dashboard' && !currentUserId ? 'opacity-60' : ''}`;

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 ease-out ${
        scrolled ? 'py-2' : 'py-4'
      }`}
    >
      <div
        className={`mx-auto transition-all duration-300 ease-out ${
          scrolled ? 'max-w-5xl px-3 sm:px-4' : 'max-w-6xl px-4 sm:px-6 lg:px-8'
        }`}
      >
        {/* The glass pill */}
        <div
          className={`flex items-center justify-between gap-3 rounded-full border backdrop-blur-xl backdrop-saturate-150 transition-all duration-300 ease-out ${
            scrolled
              ? 'h-12 pl-5 pr-2.5 bg-white/75 border-[#e6dfd8] shadow-[0_8px_30px_rgba(20,20,19,0.10)]'
              : 'h-16 pl-6 pr-3 bg-white/50 border-[#e6dfd8]/70 shadow-[0_2px_10px_rgba(20,20,19,0.04)]'
          }`}
        >
          {/* Wordmark */}
          <button
            onClick={() => handleNavClick('home')}
            className="flex items-baseline gap-1.5 cursor-pointer group select-none shrink-0"
          >
            <span
              className={`font-bold tracking-tight text-[#141413] group-hover:text-[#cc785c] transition-all duration-300 ease-out ${
                scrolled ? 'text-[15px]' : 'text-lg'
              }`}
            >
              CareerCompass
            </span>
            <span
              className={`font-semibold uppercase tracking-wider text-[#cc785c] rounded-full bg-[#f5f0e8] border border-[#e6dfd8] transition-all duration-300 ease-out ${
                scrolled ? 'text-[9px] px-1.5 py-0' : 'text-xs px-1.5 py-0.5'
              }`}
            >
              AI
            </span>
          </button>

          {/* Desktop tabs */}
          <nav className="hidden md:flex items-center gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleNavClick(tab.id)}
                className={tabClass(tab.id)}
              >
                {tab.label}
                {tab.id === 'dashboard' && currentUserId && (
                  <span className="ml-1.5 inline-block w-1.5 h-1.5 rounded-full bg-[#cc785c] align-middle" />
                )}
              </button>
            ))}
          </nav>

          {/* Status + CTA */}
          <div className="flex items-center gap-2 shrink-0">
            {/* Engine health */}
            <div
              className={`inline-flex items-center gap-2 rounded-full border font-medium transition-all duration-300 ease-out ${
                scrolled ? 'px-2.5 py-0.5' : 'px-3 py-1'
              } ${
                backendOnline === true
                  ? 'bg-[#f5f0e8]/80 text-[#252523] border-[#e6dfd8]'
                  : backendOnline === false
                  ? 'bg-rose-50/80 text-rose-800 border-rose-200'
                  : 'bg-[#f5f0e8]/80 text-[#6c6a64] border-[#e6dfd8]'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full transition-colors ${
                  backendOnline === true
                    ? 'bg-[#5db872] ring-2 ring-[#5db872]/20 animate-pulse'
                    : backendOnline === false
                    ? 'bg-[#c64545]'
                    : 'bg-[#8e8b82] animate-pulse'
                }`}
              />
              <span
                className={`hidden lg:inline font-mono transition-all duration-300 ease-out ${
                  scrolled ? 'text-[10px]' : 'text-[11px]'
                }`}
              >
                {backendOnline === true
                  ? 'Engine Online'
                  : backendOnline === false
                  ? 'Engine Offline'
                  : 'Connecting...'}
              </span>
            </div>

            {/* Primary action */}
            <button
              onClick={() => handleNavClick('profile')}
              className={`hidden sm:inline-flex items-center gap-1.5 rounded-full font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] active:bg-[#8f4730] shadow-xs cursor-pointer transition-all duration-300 ease-out hover:-translate-y-px hover:shadow-md ${
                scrolled ? 'px-3 py-1.5 text-[11px]' : 'px-4 py-2 text-xs'
              }`}
            >
              <span>Get Evaluated</span>
              <ArrowUpRight
                className={`transition-all duration-300 ease-out ${
                  scrolled ? 'w-3 h-3' : 'w-3.5 h-3.5'
                }`}
              />
            </button>

            {/* Mobile toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-[#3d3d3a] hover:text-[#141413] hover:bg-[#f5f0e8] rounded-full cursor-pointer transition-colors"
              aria-label="Toggle menu"
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile drawer: a second glass card that expands under the pill */}
        <div
          className={`md:hidden overflow-hidden transition-all duration-300 ease-out ${
            mobileMenuOpen ? 'max-h-72 opacity-100 mt-2' : 'max-h-0 opacity-0 mt-0'
          }`}
        >
          <div className="rounded-2xl border border-[#e6dfd8] bg-white/80 backdrop-blur-xl p-2 space-y-1 shadow-[0_8px_30px_rgba(20,20,19,0.08)]">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleNavClick(tab.id)}
                className={`w-full text-left px-3.5 py-2.5 rounded-xl text-sm font-medium transition-colors cursor-pointer ${
                  activePage === tab.id
                    ? 'bg-[#141413] text-[#faf9f5] font-semibold'
                    : 'text-[#3d3d3a] hover:bg-[#f5f0e8]'
                }`}
              >
                {tab.label}
                {tab.id === 'dashboard' && currentUserId && (
                  <span className="ml-2 text-[10px] font-mono opacity-70">active</span>
                )}
              </button>
            ))}

            <button
              onClick={() => handleNavClick('profile')}
              className="w-full inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] transition-colors cursor-pointer mt-1"
            >
              <span>Get Evaluated</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
