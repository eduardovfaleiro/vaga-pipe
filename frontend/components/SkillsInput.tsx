'use client';

import { KeyboardEvent, useState } from 'react';

interface SkillsInputProps {
  skills: string[];
  onChange: (skills: string[]) => void;
}

export function SkillsInput({ skills, onChange }: SkillsInputProps) {
  const [input, setInput] = useState('');

  function addSkill(value: string) {
    const trimmed = value.trim();
    if (trimmed && !skills.includes(trimmed)) {
      onChange([...skills, trimmed]);
    }
    setInput('');
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addSkill(input);
    } else if (e.key === 'Backspace' && !input && skills.length > 0) {
      onChange(skills.slice(0, -1));
    }
  }

  function removeSkill(skill: string) {
    onChange(skills.filter((s) => s !== skill));
  }

  return (
    <div className="border border-zinc-300 rounded-md p-2 flex flex-wrap gap-1.5 focus-within:border-zinc-900 transition-colors">
      {skills.map((skill) => (
        <span
          key={skill}
          className="flex items-center gap-1 bg-zinc-100 text-zinc-700 text-sm px-2 py-0.5 rounded"
        >
          {skill}
          <button
            type="button"
            onClick={() => removeSkill(skill)}
            className="text-zinc-400 hover:text-zinc-700 leading-none"
          >
            ×
          </button>
        </span>
      ))}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        onBlur={() => addSkill(input)}
        placeholder={skills.length === 0 ? 'Ex: Python, React (Enter ou vírgula)' : ''}
        className="flex-1 min-w-[120px] outline-none text-sm bg-transparent text-zinc-900 placeholder:text-zinc-400"
      />
    </div>
  );
}
