"use client";
interface StatePanelProps {
  loading: boolean;
  error: string | null;
  empty: boolean;
}

export default function StatePanel({ loading, error, empty }: StatePanelProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
        <span className="ml-4 text-primary">Generating your plan...</span>
      </div>
    );
  }
  if (error) {
    return (
      <div className="p-4 bg-warning rounded-md text-white">
        <p>{error}</p>
      </div>
    );
  }
  if (empty) {
    return (
      <div className="p-4 bg-muted rounded-md text-center">
        <p className="text-muted">Your study plan will appear here after you upload a syllabus.</p>
      </div>
    );
  }
  return null;
}