"use client";
import { useEffect, useState } from "react";
import type { RevisionCard } from '@/lib/types';

export default function CollectionPanel() {
  const [cards, setCards] = useState<RevisionCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCards = async () => {
      try {
        const res = await fetch('/api/revision-cards');
        if (!res.ok) throw new Error('Failed to load cards');
        const data = await res.json();
        setCards(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    loadCards();
  }, []);

  if (loading) return <p className="text-muted">Loading saved revision cards...</p>;
  if (error) return <p className="text-red-600">{error}</p>;
  if (cards.length === 0)
    return (
      <div className="p-4 bg-muted rounded-md text-center">
        <p>No revision cards saved yet. Create some from your study plan!</p>
      </div>
    );

  return (
    <section className="bg-card rounded-lg p-6 shadow-md mt-8">
      <h2 className="text-2xl font-semibold mb-4 text-foreground">Saved Revision Cards</h2>
      <ul className="space-y-2">
        {cards.map((card) => (
          <li key={card.card_id} className="border border-border rounded p-3">
            <div className="font-medium text-primary mb-1">{card.front}</div>
            <div className="text-muted">{card.back}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}