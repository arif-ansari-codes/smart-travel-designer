"use client";

import { useState } from "react";
import { TripForm } from "@/components/TripForm";
import { TripResults } from "@/components/TripResults";
import { TripSkeleton } from "@/components/TripSkeleton";
import { fetchTripPlan, TripApiError } from "@/services/tripApi";
import type { TripPlanResponse } from "@/types/api";
import type { TripFormValues } from "@/lib/tripSchema";

export default function TripPlanner() {
  const [result, setResult] = useState<TripPlanResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submittedDays, setSubmittedDays] = useState(1);

  const handleSubmit = async (data: TripFormValues) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setSubmittedDays(data.days);

    try {
      const response = await fetchTripPlan(data);
      setResult(response);
    } catch (err) {
      if (err instanceof TripApiError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Smart Travel Designer</h1>

      <TripForm onSubmit={handleSubmit} isLoading={loading} />

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {loading && <TripSkeleton />}

      {result && <TripResults data={result} days={submittedDays} />}
    </div>
  );
}
