"use client";
import { useState } from "react";
import type { StudyPlan } from '@/lib/types';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

interface PlannerProps {
  plan: StudyPlan;
}

export default function Planner({ plan }: PlannerProps) {
  const [topics, setTopics] = useState(plan.topics);

  const toggleComplete = (topicId: string) => {
    setTopics((prev) =>
      prev.map((t) =>
        t.topic_id === topicId ? { ...t, completion_status: !t.completion_status } : t
      )
    );
  };

  return (
    <section className="bg-card rounded-lg p-6 shadow-md">
      <h2 className="text-2xl font-semibold mb-4 text-foreground">
        7‑Day Study Planner
      </h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {topics.map((topic) => (
          <div key={topic.topic_id} className="border border-border rounded p-4">
            <div className="flex justify-between items-center mb-2">
              <h3 className="font-medium text-primary">{topic.name}</h3>
              {topic.completion_status ? (
                <CheckCircleIcon className="w-5 h-5 text-success" />
              ) : (
                <XCircleIcon className="w-5 h-5 text-muted" />
              )}
            </div>
            <div className="space-y-1">
              {topic.study_days.map((day) => (
                <div key={day} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={topic.completion_status}
                    onChange={() => toggleComplete(topic.topic_id)}
                    className="mr-2"
                  />
                  <span className="text-sm text-muted">{new Date(day).toLocaleDateString()}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}