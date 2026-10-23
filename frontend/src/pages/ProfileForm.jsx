/**
 * pages/ProfileForm.jsx
 * ---------------------
 * Student profile creation form designed with Claude's warm editorial principles.
 * Hairline borders, cream surfaces (#faf9f5, #efe9de), coral CTAs (#cc785c),
 * and accessible selectable skill pills.
 */

import React, { useState, useEffect } from 'react';
import { 
  User, 
  GraduationCap, 
  Code, 
  Heart, 
  Target, 
  ArrowRight, 
  AlertCircle, 
  Check, 
  Loader2 
} from 'lucide-react';
import { fetchCareersCatalog, createUserProfile } from '../services/api';

const EDUCATION_OPTIONS = [
  "Bachelor of Technology (B.Tech / B.E.) in Computer Science / IT",
  "Bachelor of Science (B.Sc) in Computer Science / IT",
  "Bachelor of Computer Applications (BCA)",
  "Bachelor's Degree in Statistics / Mathematics / Economics",
  "Master of Computer Applications (MCA)",
  "Master of Technology (M.Tech) / M.S. in CS / AI / Data Science",
  "Diploma in Computer Engineering / Information Technology",
  "High School / Pre-University",
  "Other Graduate / Postgraduate Degree"
];

const DEFAULT_SKILLS = [
  "Python", "Java", "SQL", "Git", "HTML", "CSS", "JavaScript", 
  "React", "Node.js", "Data Structures & Algorithms", "Excel", 
  "Data Visualization", "Power BI", "Statistics", "Mathematics", 
  "Machine Learning", "Deep Learning", "Network Security", "Linux", 
  "Ethical Hacking", "Cryptography", "SIEM"
];

const DEFAULT_INTERESTS = [
  "Software Architecture", "Coding", "Problem Solving", "Open Source",
  "Web Applications", "UI/UX Design", "Frontend Development", "Creative Design",
  "Data Analysis", "Business Intelligence", "Artificial Intelligence", 
  "Machine Learning", "Research", "Cybersecurity", "Information Security", 
  "Network Defense"
];

export default function ProfileForm({ onProfileCreated, onCancel }) {
  const [name, setName] = useState('');
  const [education, setEducation] = useState('');
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [careerGoal, setCareerGoal] = useState('');

  const [availableSkills, setAvailableSkills] = useState(DEFAULT_SKILLS);
  const [availableInterests, setAvailableInterests] = useState(DEFAULT_INTERESTS);

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [validationErrors, setValidationErrors] = useState({});

  useEffect(() => {
    let isMounted = true;
    fetchCareersCatalog()
      .then((data) => {
        if (!isMounted || !data?.careers) return;

        const skillsSet = new Set();
        const interestsSet = new Set();

        data.careers.forEach((career) => {
          (career.required_skills || []).forEach((s) => skillsSet.add(s));
          (career.relevant_interests || []).forEach((i) => interestsSet.add(i));
        });

        if (skillsSet.size > 0) setAvailableSkills(Array.from(skillsSet));
        if (interestsSet.size > 0) setAvailableInterests(Array.from(interestsSet));
      })
      .catch((err) => {
        console.warn('Backend catalog unavailable, using default skills list:', err.message);
      });

    return () => {
      isMounted = false;
    };
  }, []);

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
        career_goal: careerGoal.trim()
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

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 sm:py-14">
      
      {/* Form Header */}
      <div className="text-center mb-8 space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[#efe9de] text-[#141413] border border-[#e6dfd8]">
          <User className="w-3.5 h-3.5 text-[#cc785c]" />
          <span>Profile Configuration</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-editorial font-normal text-[#141413] tracking-tight">
          Create Your Student Profile
        </h2>
        <p className="text-xs text-[#6c6a64] max-w-md mx-auto leading-relaxed">
          Provide your current academic degree and competencies. Our rule-based engine will 
          evaluate compatibility across all industry career tracks.
        </p>
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

      {/* Form Card with Hairline Border */}
      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-[#e6dfd8] shadow-2xs p-6 sm:p-8 space-y-7">
        
        {/* 1. Full Name */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
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

        {/* 2. Education Level */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
            <GraduationCap className="w-3.5 h-3.5 text-[#cc785c]" />
            Current / Completed Degree <span className="text-[#c64545]">*</span>
          </label>
          <select
            value={education}
            onChange={(e) => setEducation(e.target.value)}
            className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all ${
              validationErrors.education ? 'border-[#c64545]' : 'border-[#e6dfd8]'
            }`}
          >
            <option value="">-- Select Your Degree Level --</option>
            {EDUCATION_OPTIONS.map((edu) => (
              <option key={edu} value={edu}>
                {edu}
              </option>
            ))}
          </select>
          {validationErrors.education && (
            <p className="text-xs text-[#c64545] mt-1.5 flex items-center gap-1 font-medium">
              <AlertCircle className="w-3 h-3" /> {validationErrors.education}
            </p>
          )}
        </div>

        {/* 3. Existing Skills Multi-select */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-[#141413] flex items-center gap-1.5">
              <Code className="w-3.5 h-3.5 text-[#cc785c]" />
              Current Technical Skills
            </label>
            <span className="text-[11px] font-mono font-medium text-[#252523] bg-[#efe9de] px-2 py-0.5 rounded-full border border-[#e6dfd8]">
              {selectedSkills.length} selected
            </span>
          </div>
          <p className="text-xs text-[#6c6a64] mb-3">
            Select the languages, libraries, and tools you have experience with:
          </p>

          <div className="flex flex-wrap gap-2 max-h-56 overflow-y-auto p-3.5 rounded-lg border border-[#e6dfd8] bg-[#faf9f5]">
            {availableSkills.map((skill) => {
              const isSelected = selectedSkills.includes(skill);
              return (
                <button
                  type="button"
                  key={skill}
                  onClick={() => handleToggleSkill(skill)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#cc785c] text-white border-[#cc785c] shadow-xs'
                      : 'bg-white text-[#3d3d3a] border-[#e6dfd8] hover:border-[#cc785c]/60 hover:bg-[#f5f0e8]'
                  }`}
                >
                  {isSelected && <Check className="w-3 h-3 text-white stroke-[2.5]" />}
                  <span>{skill}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* 4. Interests Multi-select */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-[#141413] flex items-center gap-1.5">
              <Heart className="w-3.5 h-3.5 text-[#cc785c]" />
              Professional Interests
            </label>
            <span className="text-[11px] font-mono font-medium text-[#252523] bg-[#efe9de] px-2 py-0.5 rounded-full border border-[#e6dfd8]">
              {selectedInterests.length} selected
            </span>
          </div>
          <p className="text-xs text-[#6c6a64] mb-3">
            Select the domain areas that genuinely interest you:
          </p>

          <div className="flex flex-wrap gap-2 max-h-56 overflow-y-auto p-3.5 rounded-lg border border-[#e6dfd8] bg-[#faf9f5]">
            {availableInterests.map((interest) => {
              const isSelected = selectedInterests.includes(interest);
              return (
                <button
                  type="button"
                  key={interest}
                  onClick={() => handleToggleInterest(interest)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#141413] text-[#faf9f5] border-[#141413] shadow-xs'
                      : 'bg-white text-[#3d3d3a] border-[#e6dfd8] hover:border-[#141413]/50 hover:bg-[#f5f0e8]'
                  }`}
                >
                  {isSelected && <Check className="w-3 h-3 text-white stroke-[2.5]" />}
                  <span>{interest}</span>
                </button>
              );
            })}
          </div>
          {validationErrors.skills && (
            <p className="text-xs text-[#c64545] mt-2 font-medium flex items-center gap-1">
              <AlertCircle className="w-3 h-3" /> {validationErrors.skills}
            </p>
          )}
        </div>

        {/* 5. Career Goal (Optional) */}
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-[#141413] mb-1.5 flex items-center gap-1.5">
            <Target className="w-3.5 h-3.5 text-[#cc785c]" />
            Target Career Goal <span className="text-[10px] text-[#8e8b82] font-normal lowercase">(optional)</span>
          </label>
          <input
            type="text"
            value={careerGoal}
            onChange={(e) => setCareerGoal(e.target.value)}
            placeholder="e.g. AI/ML Engineer or Data Analyst"
            className="w-full px-3.5 py-2.5 rounded-lg border border-[#e6dfd8] text-sm text-[#141413] bg-[#faf9f5] focus:outline-hidden focus:border-[#cc785c] focus:ring-2 focus:ring-[#cc785c]/15 transition-all"
          />
        </div>

        {/* Action Buttons */}
        <div className="pt-4 flex flex-col sm:flex-row items-center justify-end gap-3 border-t border-[#e6dfd8]">
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
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-2.5 rounded-lg text-xs font-semibold text-white bg-[#cc785c] hover:bg-[#a9583e] active:bg-[#8f4730] transition-colors shadow-xs disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Saving Profile...</span>
              </>
            ) : (
              <>
                <span>Generate Recommendations</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>

      </form>

    </div>
  );
}
