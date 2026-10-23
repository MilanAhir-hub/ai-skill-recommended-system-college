/**
 * components/Loading.jsx
 * ----------------------
 * Loading state indicator styled with Claude's warm cream and coral palette.
 */

import React from 'react';
import { Loader2 } from 'lucide-react';

export default function Loading({ message = 'Evaluating profile against heuristic career knowledge base...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div className="relative mb-5">
        <div className="w-14 h-14 rounded-2xl bg-[#efe9de] border border-[#e6dfd8] flex items-center justify-center text-[#cc785c] shadow-xs">
          <Loader2 className="w-7 h-7 animate-spin" />
        </div>
      </div>
      <h3 className="text-xl font-normal text-[#141413] mb-1.5 font-editorial tracking-tight">
        Computing Explainable Match
      </h3>
      <p className="text-xs text-[#6c6a64] max-w-sm leading-relaxed">
        {message}
      </p>
    </div>
  );
}
