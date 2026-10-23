/**
 * pages/ProfileForm.jsx
 * ---------------------
 * Student profile builder designed with Claude's warm editorial principles.
 * Every option list (education, 92 skills grouped in categories, grouped
 * interests, career goals) is served by the backend knowledge base, so the
 * form can never drift from what the scoring engine actually understands.
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
  User,
  GraduationCap,
  Code,
  Heart,
  Target,
  ArrowRight,
  AlertCircle,
  Check,
  Loader2,
  Search,
  Clock,
  Flame,
  X,
  Sparkles,
  Layers
} from 'lucide-react';
import {
  fetchSkillCatalog,
  fetchInterestCatalog,
  fetchEducationOptions,
  fetchCareersCatalog,
  createUserProfile
} from '../services/api';

/* ------------------------------------------------------------------ *
 * Offline fallbacks: used only when the backend is unreachable, so the
 * form still works during a demo without the Flask server running.
 * ------------------------------------------------------------------ */
const FALLBACK_EDUCATION = [
  "Bachelor of Technology (B.Tech / B.E.) in Computer Science / IT",
  "Bachelor of Technology (B.Tech / B.E.) in Electronics / ECE / EEE",
  "Bachelor of Science (B.Sc) in Computer Science / IT",
  "Bachelor of Computer Applications (BCA)",
  "Bachelor of Commerce (B.Com) / BBA / Management",
  "Bachelor of Design (B.Des) / Fine Arts / Animation",
  "Master of Computer Applications (MCA)",
  "Master of Technology (M.Tech) / M.S. in CS / AI / Data Science",
  "Master of Business Administration (MBA)",
  "Diploma in Computer Engineering / Information Technology",
  "High School / Pre-University",
  "Other Graduate / Postgraduate Degree"
];

const FALLBACK_SKILL_CATEGORIES = {
  "Programming Languages": [
    { skill: "Python", difficulty: "Beginner", learning_hours: 60, required_by_careers: 9 },
    { skill: "Java", difficulty: "Beginner", learning_hours: 80, required_by_careers: 1 },
    { skill: "JavaScript", difficulty: "Beginner", learning_hours: 70, required_by_careers: 3 }
  ],
  "Web & Frontend": [
    { skill: "HTML", difficulty: "Beginner", learning_hours: 25, required_by_careers: 3 },
    { skill: "CSS", difficulty: "Beginner", learning_hours: 40, required_by_careers: 3 },
    { skill: "React", difficulty: "Intermediate", learning_hours: 70, required_by_careers: 2 }
  ],
  "Databases": [
    { skill: "SQL", difficulty: "Beginner", learning_hours: 50, required_by_careers: 11 }
  ],
  "Cloud & DevOps": [
    { skill: "Git", difficulty: "Beginner", learning_hours: 20, required_by_careers: 10 },
    { skill: "Linux", difficulty: "Beginner", learning_hours: 40, required_by_careers: 6 }
  ]
};

const FALLBACK_INTEREST_GROUPS = {
  "Engineering & Building": ["Coding", "Problem Solving", "Software Architecture", "Scalable Systems", "Open Source"],
  "Web, Mobile & Design": ["Web Applications", "Frontend Development", "Mobile Development", "UI/UX Design", "Creative Design"],
  "Data & AI": ["Data Analysis", "Data Science", "Business Intelligence", "Statistics", "Machine Learning", "Artificial Intelligence"],
  "Infrastructure & Security": ["Cloud Computing", "DevOps & Automation", "Networking", "Cybersecurity", "Ethical Hacking"],
  "Business & Product": ["Business Strategy", "Product Management", "Quality Assurance"],
  "Emerging & Specialised": ["Game Development", "Blockchain & Web3", "Internet of Things", "Hardware & Electronics", "Robotics"]
};

const PACE_OPTIONS = [
  { value: 5, label: '5 hrs / week', hint: 'Alongside a full college load' },
  { value: 10, label: '10 hrs / week', hint: 'Balanced and realistic' },
  { value: 15, label: '15 hrs / week', hint: 'Focused preparation' },
  { value: 20, label: '20 hrs / week', hint: 'Intensive' },
  { value: 30, label: '30 hrs / week', hint: 'Full-time placement prep' }
];

const DIFFICULTY_DOT = {
  Beginner: 'bg-[#5db872]',
  Intermediate: 'bg-[#e8a55a]',
  Advanced: 'bg-[#c64545]'
};

export default function ProfileForm({ onProfileCreated, onCancel }) {
  const [name, setName] = useState('');
  const [education, setEducation] = useState('');
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [careerGoal, setCareerGoal] = useState('');
  const [hoursPerWeek, setHoursPerWeek] = useState(10);

  const [educationOptions, setEducationOptions] = useState(FALLBACK_EDUCATION);
  const [skillCategories, setSkillCategories] = useState(FALLBACK_SKILL_CATEGORIES);
  const [interestGroups, setInterestGroups] = useState(FALLBACK_INTEREST_GROUPS);
  const [topSkills, setTopSkills] = useState([]);
  const [careerTitles, setCareerTitles] = useState([]);

  const [skillQuery, setSkillQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [validationErrors, setValidationErrors] = useState({});

  /* Load every catalog from the backend knowledge base */
  useEffect(() => {
    let isMounted = true;

    fetchSkillCatalog()
      .then((data) => {
        if (!isMounted || !data?.categories) return;
        setSkillCategories(data.categories);
        setTopSkills((data.most_in_demand_skills || []).slice(0, 8));
      })
      .catch((err) => console.warn('Skill catalog unavailable, using fallback:', err.message));

    fetchInterestCatalog()
      .then((data) => {
        if (isMounted && data?.groups) setInterestGroups(data.groups);
      })
      .catch((err) => console.warn('Interest catalog unavailable, using fallback:', err.message));

    fetchEducationOptions()
      .then((data) => {
        if (isMounted && data?.options?.length) setEducationOptions(data.options);
      })
      .catch((err) => console.warn('Education options unavailable, using fallback:', err.message));

    fetchCareersCatalog({ view: 'summary' })
      .then((data) => {
        if (isMounted && data?.careers) {
          setCareerTitles(data.careers.map((career) => career.title));
        }
      })
      .catch((err) => console.warn('Career catalog unavailable:', err.message));

    return () => { isMounted = false; };
  }, []);

  const categoryNames = useMemo(
    () => ['All', ...Object.keys(skillCategories).sort()],
    [skillCategories]
  );

  /* Flatten + filter the skill catalog for the current tab and search box */
  const visibleSkills = useMemo(() => {
    const query = skillQuery.trim().toLowerCase();

    const entries = Object.entries(skillCategories)
      .filter(([category]) => activeCategory === 'All' || category === activeCategory)
      .map(([category, skills]) => [
        category,
        skills.filter((item) => !query || item.skill.toLowerCase().includes(query))
      ])
      .filter(([, skills]) => skills.length > 0);

    return entries.sort((a, b) => a[0].localeCompare(b[0]));
  }, [skillCategories, activeCategory, skillQuery]);

  const totalSkillCount = useMemo(
    () => Object.values(skillCategories).reduce((sum, skills) => sum + skills.length, 0),
    [skillCategories]
  );

  const handleToggleSkill = (skill) => {
    setSelectedSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  const handleToggleInterest = (interest) => {
    setSelectedInterests((prev) =>
      prev.includes(interest) ? prev.filter((i) => i !== interest) : [...prev, interest]
    );
  };

  const validateForm = () => {
    const errors = {};
    if (!name.trim()) {
      errors.name = 'Full Name is required.';
    }
    if (!education) {
      errors.education = 'Please select your current education level.';
    }
    if (selectedSkills.length === 0 && selectedInterests.length === 0) {
      errors.skills = 'Please select at least one skill or interest for career matching.';
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!validateForm()) return;

    setLoading(true);

    try {
      const payload = {
        name: name.trim(),
        education,
        skills: selectedSkills,
        interests: selectedInterests,
        career_goal: careerGoal.trim(),
        hours_per_week: hoursPerWeek
      };

      const response = await createUserProfile(payload);
      const createdUser = response.user;

      if (!createdUser || !createdUser.id) {
        throw new Error('Server did not return a valid user profile.');
      }

      onProfileCreated(createdUser.id, createdUser);

    } catch (err) {
      setErrorMessage(err.message || 'Failed to submit profile. Please verify your connection.');
    } finally {
      setLoading(false);
    }
  };

  const completion = [
    name.trim() !== '',
    education !== '',
    selectedSkills.length > 0 || selectedInterests.length > 0
  ].filter(Boolean).length;

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 sm:py-14">

      {/* Form Header */}
      <div className="text-center mb-8 space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[#efe9de] text-[#141413] border border-[#e6dfd8]">
          <User className="w-3.5 h-3.5 text-[#cc785c]" />
          <span>Profile Configuration</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-editorial font-normal text-[#141413] tracking-tight">
          Build Your Student Profile
        </h2>
        <p className="text-xs text-[#6c6a64] max-w-lg mx-auto leading-relaxed">
          Tell us what you have studied and what you can already do. The rule-based engine will score
          you against every career track and generate a phased career path for your best matches.
        </p>

        {/* Completion indicator */}
        <div className="pt-3 max-w-xs mx-auto space-y-1.5">
          <div className="w-full bg-[#efe9de] h-1.5 rounded-full overflow-hidden border border-[#e6dfd8]/60">
            <div
              className="h-full rounded-full bg-[#cc785c] transition-all duration-500"
              style={{ width: `${(completion / 3) * 100}%` }}
            />
          </div>
          <p className="text-[11px] font-mono text-[#8e8b82]">
            {completion} of 3 required sections complete
          </p>
        </div>
      </div>

      {/* Global Error Banner */}
      {errorMessage && (
        <div className="mb-6 p-4 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold">Notice: </span>
            <span>{errorMessage}</span>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">

        {/* Section 1: Identity & education */}
        <div className="bg-white rounded-xl border border-[#e6dfd8] shadow-2xs p-6 sm:p-8 space-y-6">
          <div className="flex items-center gap-2 pb-3 border-b border-[#e6dfd8]">
            <span className="w-6 h-6 rounded-full bg-[#efe9de] text-[#cc785c] font-mono text-[11px] font-bold flex items-center justify-center">
              1
            </span>
            <h3 className="text-base font-semibold text-[#141413]">About you</h3>
          </div>

          {/* Full Name */}
          <div>
            <label className="text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
              <User className="w-3.5 h-3.5 text-[#cc785c]" />
              Full Name <span className="text-[#c64545]">*</span>
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Milan Gagiya"
              className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all ${
                validationErrors.name ? 'border-[#c64545]' : 'border-[#e6dfd8]'
              }`}
            />
            {validationErrors.name && (
              <p className="text-xs text-[#c64545] mt-1.5 flex items-center gap-1 font-medium">
                <AlertCircle className="w-3 h-3" /> {validationErrors.name}
              </p>
            )}
          </div>

          {/* Education Level */}
          <div>
            <label className="text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
              <GraduationCap className="w-3.5 h-3.5 text-[#cc785c]" />
              Current / Completed Degree <span className="text-[#c64545]">*</span>
            </label>
            <select
              value={education}
              onChange={(e) => setEducation(e.target.value)}
              className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all cursor-pointer ${
                validationErrors.education ? 'border-[#c64545]' : 'border-[#e6dfd8]'
              }`}
            >
              <option value="">-- Select Your Degree Level --</option>
              {educationOptions.map((edu) => (
                <option key={edu} value={edu}>{edu}</option>
              ))}
            </select>
            <p className="text-[11px] text-[#8e8b82] mt-1.5">
              Non-CS degrees are fully supported: commerce, design, electronics and management each unlock their own tracks.
            </p>
            {validationErrors.education && (
              <p className="text-xs text-[#c64545] mt-1.5 flex items-center gap-1 font-medium">
                <AlertCircle className="w-3 h-3" /> {validationErrors.education}
              </p>
            )}
          </div>
        </div>

        {/* Section 2: Skills */}
        <div className="bg-white rounded-xl border border-[#e6dfd8] shadow-2xs p-6 sm:p-8 space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[#e6dfd8]">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-[#efe9de] text-[#cc785c] font-mono text-[11px] font-bold flex items-center justify-center">
                2
              </span>
              <h3 className="text-base font-semibold text-[#141413] flex items-center gap-1.5">
                <Code className="w-4 h-4 text-[#cc785c]" />
                Skills you already have
              </h3>
            </div>
            <span className="text-[11px] font-mono font-medium text-[#252523] bg-[#efe9de] px-2 py-0.5 rounded-full border border-[#e6dfd8]">
              {selectedSkills.length} of {totalSkillCount} selected
            </span>
          </div>

          {/* Selected skills summary */}
          {selectedSkills.length > 0 && (
            <div className="flex flex-wrap gap-2 p-3 bg-[#f5f0e8] border border-[#e6dfd8] rounded-lg">
              {selectedSkills.map((skill) => (
                <button
                  type="button"
                  key={skill}
                  onClick={() => handleToggleSkill(skill)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-[#cc785c] text-white hover:bg-[#a9583e] transition-colors cursor-pointer"
                >
                  <span>{skill}</span>
                  <X className="w-3 h-3" />
                </button>
              ))}
              <button
                type="button"
                onClick={() => setSelectedSkills([])}
                className="text-[11px] text-[#6c6a64] hover:text-[#141413] underline underline-offset-2 px-1 cursor-pointer"
              >
                Clear all
              </button>
            </div>
          )}

          {/* Most in-demand quick picks */}
          {topSkills.length > 0 && (
            <div className="space-y-2">
              <p className="text-[11px] font-semibold uppercase tracking-wider text-[#8e8b82] flex items-center gap-1.5">
                <Flame className="w-3.5 h-3.5 text-[#cc785c]" />
                Most in demand across all career tracks
              </p>
              <div className="flex flex-wrap gap-2">
                {topSkills.map((item) => {
                  const isSelected = selectedSkills.includes(item.skill);
                  return (
                    <button
                      type="button"
                      key={item.skill}
                      onClick={() => handleToggleSkill(item.skill)}
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                        isSelected
                          ? 'bg-[#cc785c] text-white border-[#cc785c]'
                          : 'bg-[#faf9f5] text-[#3d3d3a] border-[#e6dfd8] hover:border-[#cc785c]/60'
                      }`}
                    >
                      {isSelected && <Check className="w-3 h-3 stroke-[2.5]" />}
                      <span>{item.skill}</span>
                      <span className={`text-[10px] font-mono ${isSelected ? 'text-white/70' : 'text-[#8e8b82]'}`}>
                        {item.required_by} roles
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Search + category filter */}
          <div className="space-y-3">
            <div className="relative">
              <Search className="w-4 h-4 text-[#8e8b82] absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={skillQuery}
                onChange={(e) => setSkillQuery(e.target.value)}
                placeholder="Search skills (react, sql, docker, figma...)"
                className="w-full pl-9 pr-3 py-2.5 rounded-lg border border-[#e6dfd8] text-sm text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all"
              />
            </div>

            <div className="flex flex-wrap gap-1.5">
              {categoryNames.map((category) => (
                <button
                  type="button"
                  key={category}
                  onClick={() => setActiveCategory(category)}
                  className={`px-2.5 py-1 rounded-md text-[11px] font-medium border transition-colors cursor-pointer ${
                    activeCategory === category
                      ? 'bg-[#141413] text-[#faf9f5] border-[#141413]'
                      : 'bg-[#faf9f5] text-[#6c6a64] border-[#e6dfd8] hover:bg-[#f5f0e8] hover:text-[#141413]'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Grouped skill picker */}
          <div className="max-h-96 overflow-y-auto rounded-lg border border-[#e6dfd8] bg-[#faf9f5] divide-y divide-[#e6dfd8]">
            {visibleSkills.length === 0 && (
              <p className="p-4 text-xs text-[#8e8b82] italic">
                No skills match "{skillQuery}". Try a shorter search.
              </p>
            )}

            {visibleSkills.map(([category, skills]) => (
              <div key={category} className="p-3.5 space-y-2">
                <p className="text-[11px] font-semibold uppercase tracking-wider text-[#8e8b82] flex items-center gap-1.5">
                  <Layers className="w-3 h-3 text-[#cc785c]" />
                  {category}
                  <span className="font-mono font-normal normal-case tracking-normal">({skills.length})</span>
                </p>
                <div className="flex flex-wrap gap-2">
                  {skills.map((item) => {
                    const isSelected = selectedSkills.includes(item.skill);
                    return (
                      <button
                        type="button"
                        key={item.skill}
                        onClick={() => handleToggleSkill(item.skill)}
                        title={`${item.difficulty} - about ${item.learning_hours} hrs to learn - required by ${item.required_by_careers} career(s)`}
                        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                          isSelected
                            ? 'bg-[#cc785c] text-white border-[#cc785c] shadow-xs'
                            : 'bg-white text-[#3d3d3a] border-[#e6dfd8] hover:border-[#cc785c]/60 hover:bg-[#f5f0e8]'
                        }`}
                      >
                        {isSelected
                          ? <Check className="w-3 h-3 text-white stroke-[2.5]" />
                          : <span className={`w-1.5 h-1.5 rounded-full ${DIFFICULTY_DOT[item.difficulty] || 'bg-[#d6cbbe]'}`} />}
                        <span>{item.skill}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          <div className="flex flex-wrap items-center gap-3 text-[11px] text-[#8e8b82]">
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#5db872]" /> Beginner
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#e8a55a]" /> Intermediate
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#c64545]" /> Advanced
            </span>
            <span className="ml-auto">Hover a skill for hours and demand.</span>
          </div>
        </div>

        {/* Section 3: Interests */}
        <div className="bg-white rounded-xl border border-[#e6dfd8] shadow-2xs p-6 sm:p-8 space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[#e6dfd8]">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-[#efe9de] text-[#cc785c] font-mono text-[11px] font-bold flex items-center justify-center">
                3
              </span>
              <h3 className="text-base font-semibold text-[#141413] flex items-center gap-1.5">
                <Heart className="w-4 h-4 text-[#cc785c]" />
                What genuinely interests you
              </h3>
            </div>
            <span className="text-[11px] font-mono font-medium text-[#252523] bg-[#efe9de] px-2 py-0.5 rounded-full border border-[#e6dfd8]">
              {selectedInterests.length} selected
            </span>
          </div>

          <p className="text-xs text-[#6c6a64] leading-relaxed">
            Interests carry 30% of the score, so pick the work you would happily do on a Sunday, not the one that sounds impressive.
          </p>

          <div className="space-y-4">
            {Object.entries(interestGroups).map(([group, interests]) => (
              <div key={group} className="space-y-2">
                <p className="text-[11px] font-semibold uppercase tracking-wider text-[#8e8b82]">
                  {group}
                </p>
                <div className="flex flex-wrap gap-2">
                  {interests.map((interest) => {
                    const isSelected = selectedInterests.includes(interest);
                    return (
                      <button
                        type="button"
                        key={interest}
                        onClick={() => handleToggleInterest(interest)}
                        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                          isSelected
                            ? 'bg-[#141413] text-[#faf9f5] border-[#141413] shadow-xs'
                            : 'bg-[#faf9f5] text-[#3d3d3a] border-[#e6dfd8] hover:border-[#141413]/50 hover:bg-[#f5f0e8]'
                        }`}
                      >
                        {isSelected && <Check className="w-3 h-3 text-white stroke-[2.5]" />}
                        <span>{interest}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {validationErrors.skills && (
            <p className="text-xs text-[#c64545] font-medium flex items-center gap-1">
              <AlertCircle className="w-3 h-3" /> {validationErrors.skills}
            </p>
          )}
        </div>

        {/* Section 4: Goal & pace */}
        <div className="bg-white rounded-xl border border-[#e6dfd8] shadow-2xs p-6 sm:p-8 space-y-6">
          <div className="flex items-center gap-2 pb-3 border-b border-[#e6dfd8]">
            <span className="w-6 h-6 rounded-full bg-[#efe9de] text-[#cc785c] font-mono text-[11px] font-bold flex items-center justify-center">
              4
            </span>
            <h3 className="text-base font-semibold text-[#141413]">Goal and study pace</h3>
          </div>

          {/* Career Goal */}
          <div>
            <label className="text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-[#cc785c]" />
              Target Career Goal
              <span className="text-[10px] text-[#8e8b82] font-normal lowercase">(optional)</span>
            </label>
            <input
              type="text"
              list="career-goal-options"
              value={careerGoal}
              onChange={(e) => setCareerGoal(e.target.value)}
              placeholder="e.g. AI/ML Engineer, Data Analyst, SDET, MERN Developer"
              className="w-full px-3.5 py-2.5 rounded-lg border border-[#e6dfd8] text-sm text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all"
            />
            <datalist id="career-goal-options">
              {careerTitles.map((title) => (
                <option key={title} value={title} />
              ))}
            </datalist>
            <p className="text-[11px] text-[#8e8b82] mt-1.5 flex items-start gap-1.5">
              <Sparkles className="w-3 h-3 text-[#cc785c] shrink-0 mt-0.5" />
              <span>
                Job-title synonyms are understood, so "ML Engineer", "SDET" or "full stack developer" all resolve correctly.
              </span>
            </p>

            {careerTitles.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-2.5">
                {careerTitles.slice(0, 8).map((title) => (
                  <button
                    type="button"
                    key={title}
                    onClick={() => setCareerGoal(title)}
                    className={`px-2.5 py-1 rounded-md text-[11px] font-medium border transition-colors cursor-pointer ${
                      careerGoal === title
                        ? 'bg-[#f5f0e8] text-[#a9583e] border-[#cc785c]/50'
                        : 'bg-[#faf9f5] text-[#6c6a64] border-[#e6dfd8] hover:bg-[#f5f0e8] hover:text-[#141413]'
                    }`}
                  >
                    {title}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Study pace */}
          <div>
            <label className="text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-[#cc785c]" />
              Study hours you can commit per week
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
              {PACE_OPTIONS.map((option) => (
                <button
                  type="button"
                  key={option.value}
                  onClick={() => setHoursPerWeek(option.value)}
                  className={`px-2.5 py-2 rounded-lg text-left border transition-all cursor-pointer ${
                    hoursPerWeek === option.value
                      ? 'bg-[#f5f0e8] border-[#cc785c]/60 ring-2 ring-[#cc785c]/10'
                      : 'bg-[#faf9f5] border-[#e6dfd8] hover:border-[#cc785c]/40'
                  }`}
                >
                  <div className="text-xs font-semibold text-[#141413]">{option.label}</div>
                  <div className="text-[10px] text-[#8e8b82] leading-tight mt-0.5">{option.hint}</div>
                </button>
              ))}
            </div>
            <p className="text-[11px] text-[#8e8b82] mt-2">
              This converts your learning hours into real weeks and months. You can change it later on the dashboard.
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-end gap-3">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="w-full sm:w-auto px-5 py-2.5 rounded-lg text-xs font-semibold text-[#6c6a64] hover:text-[#141413] hover:bg-[#f5f0e8] transition-colors cursor-pointer"
            >
              Cancel
            </button>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] active:bg-[#8f4730] transition-colors shadow-xs disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Generating your career paths...</span>
              </>
            ) : (
              <>
                <span>Generate My Career Path</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>

      </form>

    </div>
  );
}
