"use client";
import { useState } from "react";
import { fetchStudyPlan } from '@/lib/api';
import { CloudUploadIcon } from '@heroicons/react/24/outline';

interface HeroProps {
  onPlanReady: (plan: any) => void;
  setLoading: (l: boolean) => void;
  setError: (e: string | null) => void;
}

export default function Hero({ onPlanReady, setLoading, setError }: HeroProps) {
  const [syllabus, setSyllabus] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!syllabus.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const plan = await fetchStudyPlan({
        user_id: 'demo-user',
        syllabus,
        start_date: new Date().toISOString().split('T')[0]
      });
      onPlanReady(plan);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-card rounded-lg p-8 shadow-md">
      <h1 className="text-4xl font-bold mb-4 text-primary">
        StudyMate
      </h1>
      <p className="text-lg text-muted mb-6">
        Your intelligent study planner – upload a syllabus and get a personalized 7‑day plan instantly.
      </p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={syllabus}
          onChange={(e) => setSyllabus(e.target.value)}
          placeholder="Paste your syllabus or exam topics here..."
          rows={6}
          className="w-full p-3 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <button
          type="submit"
          className="inline-flex items-center px-6 py-2 bg-primary text-white rounded-md hover:bg-accent transition-colors"
        >
          <CloudUploadIcon className="w-5 h-5 mr-2" />
          Generate Study Plan
        </button>
      </form>
    </section>
  );
}