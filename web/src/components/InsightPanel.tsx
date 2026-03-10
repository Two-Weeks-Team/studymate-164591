"use client";
import { useEffect, useState } from "react";

export default function InsightPanel() {
  const [insight, setInsight] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock AI insight after plan generation – replace with real call
    const timer = setTimeout(() => {
      setInsight('Focus on Chapter 3 this week for better retention based on past performance.');
      setLoading(false);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  if (loading) return null;

  return (
    <section className="bg-muted rounded-lg p-4 mt-6">
      <h3 className="font-medium text-primary mb-2">AI Insight</h3>
      <p className="text-foreground">{insight}</p>
    </section>
  );
}