"use client";
import { useState } from "react";
import Hero from '@/components/Hero';
import Planner from '@/components/Planner';
import ProgressDashboard from '@/components/ProgressDashboard';
import CollectionPanel from '@/components/CollectionPanel';
import StatsStrip from '@/components/StatsStrip';
import StatePanel from '@/components/StatePanel';
import type { StudyPlan } from '@/lib/api';

export default function HomePage() {
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePlanGenerated = (generated: StudyPlan) => {
    setPlan(generated);
    setError(null);
  };

  return (
    <main className="flex-1 container mx-auto p-4 space-y-8">
      <StatsStrip />
      <Hero onPlanReady={handlePlanGenerated} setLoading={setLoading} setError={setError} />
      <StatePanel loading={loading} error={error} empty={!plan} />
      {plan && (
        <>
          <Planner plan={plan} />
          <ProgressDashboard planId={plan.plan_id} />
        </>
      )}
      <CollectionPanel />
    </main>
  );
}