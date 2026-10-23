/**
 * components/SkillList.jsx
 * ------------------------
 * Badges for matched skills, missing skills, and interests.
 * Follows Claude-inspired warm cream pills with subtle hairline borders.
 */

import React from 'react';
import { Check, Target, Heart, Tag } from 'lucide-react';

export default function SkillList({ 
  skills = [], 
  type = 'default', // 'matched' | 'missing' | 'interest' | 'default'
  emptyMessage = 'None specified' 
}) {
  if (!skills || skills.length === 0) {
    return (
      <span className="text-xs text-[#8e8b82] italic font-serif">
        {emptyMessage}
      </span>
    );
  }

  // Styles adhering to DESIGN.md tokens
  const getBadgeStyle = () => {
    switch (type) {
      case 'matched':
        return {
          bg: 'bg-[#faf9f5] text-[#141413] border-[#d1e7d8] hover:border-[#5db872]',
          icon: <Check className="w-3.5 h-3.5 text-[#5db872] stroke-[2.5] shrink-0" />
        };
      case 'missing':
        return {
          bg: 'bg-[#faf9f5] text-[#141413] border-[#f0d8ce] hover:border-[#cc785c]',
          icon: <Target className="w-3.5 h-3.5 text-[#cc785c] shrink-0" />
        };
      case 'interest':
        return {
          bg: 'bg-[#efe9de] text-[#252523] border-[#e6dfd8]',
          icon: <Heart className="w-3.5 h-3.5 text-[#cc785c] shrink-0" />
        };
      default:
        return {
          bg: 'bg-[#f5f0e8] text-[#3d3d3a] border-[#e6dfd8]',
          icon: <Tag className="w-3.5 h-3.5 text-[#6c6a64] shrink-0" />
        };
    }
  };

  const style = getBadgeStyle();

  return (
    <div className="flex flex-wrap gap-2">
      {skills.map((skill, index) => (
        <span
          key={`${skill}-${index}`}
          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border shadow-2xs transition-colors ${style.bg}`}
        >
          {style.icon}
          <span>{skill}</span>
        </span>
      ))}
    </div>
  );
}
