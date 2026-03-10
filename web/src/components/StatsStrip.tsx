"use client";
export default function StatsStrip() {
  return (
    <section className="flex flex-wrap gap-4 justify-center">
      <div className="bg-primary text-white px-4 py-2 rounded-full shadow-md">
        AI‑Powered Plans
      </div>
      <div className="bg-accent text-white px-4 py-2 rounded-full shadow-md">
        Real‑Time Progress
      </div>
      <div className="bg-success text-white px-4 py-2 rounded-full shadow-md">
        7‑Day Scheduler
      </div>
    </section>
  );
}