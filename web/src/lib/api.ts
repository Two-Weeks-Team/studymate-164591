import type { StudyPlan, RevisionCard } from '@/lib/types';

export async function fetchStudyPlan(payload: {
  user_id: string;
  syllabus: string;
  start_date: string;
}): Promise<StudyPlan> {
  const response = await fetch('/api/study-plans', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.message || 'Failed to generate study plan');
  }
  return response.json();
}

export async function fetchRevisionCards(payload: {
  user_id: string;
  material: string;
}): Promise<RevisionCard[]> {
  const response = await fetch('/api/revision-cards', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.message || 'Failed to generate revision cards');
  }
  return response.json();
}
