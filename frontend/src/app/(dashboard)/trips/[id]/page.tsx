"use client";

import { useTrip } from "@/context/trip-context";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import Link from "next/link";

export default function TripItineraryPage() {
  const { trip } = useTrip();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Itinerary</h2>
        <Button asChild>
          {/* Link to builder or open a modal */}
          <Link href={`/trips/${trip?.id}/builder`}>
            <Plus className="mr-2 size-4" />
            Add Stop / Activity
          </Link>
        </Button>
      </div>

      <div className="border rounded-lg p-10 flex flex-col items-center justify-center text-center text-muted-foreground min-h-[300px] bg-card shadow-sm">
        <p className="mb-4">No activities added yet.</p>
        <Button variant="outline" asChild>
          <Link href={`/trips/${trip?.id}/builder`}>Start Building</Link>
        </Button>
      </div>
    </div>
  );
}
