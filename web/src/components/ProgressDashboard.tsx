"use client";
import { useEffect, useState } from "react";
import { fetch } from '@/lib/api'; // placeholder import – will use a simple fetch below
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface DashboardProps {
  planId: string;
}

interface ProgressData {
  dates: string[];
  minutes: number[];
}

export default function ProgressDashboard({ planId }: DashboardProps) {
  const [data, setData] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Simple mock fetch – replace with real endpoint when available
    const fetchData = async () => {
      try {
        const res = await fetch('/api/progress');
        if (!res.ok) throw new Error('Failed to load progress');
        const json = await res.json();
        setData({ dates: json.map((p: any) => p.study_date), minutes: json.map((p: any) => p.time_spent) });
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <p className="text-muted">Loading progress...</p>;
  if (error) return <p className="text-red-600">{error}</p>;
  if (!data) return null;

  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: 'Minutes Studied',
        data: data.minutes,
        backgroundColor: 'var(--color-primary)'
      }
    ]
  };

  return (
    <section className="bg-card rounded-lg p-6 shadow-md mt-8">
      <h2 className="text-2xl font-semibold mb-4 text-foreground">Progress Dashboard</h2>
      <Chart type="bar" data={chartData} />
    </section>
  );
}