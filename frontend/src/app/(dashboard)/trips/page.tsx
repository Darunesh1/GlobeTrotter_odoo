"use client";

import { useEffect, useState } from "react";
import { Plus, Loader2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { TripCard, Trip } from "@/components/trip-card";
import api from "@/lib/api";
import { toast } from "sonner";

export default function TripsPage() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      const { data } = await api.get("/trips");
      setTrips(data);
    } catch (error) {
      console.error("Failed to fetch trips", error);
      toast.error("Error", {
        description: "Failed to load your trips.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-primary">
            My Trips
          </h2>
          <p className="text-muted-foreground">
            Manage your travel plans and itineraries.
          </p>
        </div>
        <Button asChild className="shadow-lg shadow-primary/20">
          <Link href="/trips/create">
            <Plus className="mr-2 size-4" />
            Plan New Trip
          </Link>
        </Button>
      </div>

      {isLoading ? (
        <div className="flex h-40 items-center justify-center">
          <Loader2 className="size-8 animate-spin text-primary" />
        </div>
      ) : trips.length === 0 ? (
        <div className="flex h-64 flex-col items-center justify-center rounded-lg border border-dashed text-center animate-in fade-in-50">
          <div className="bg-primary/10 p-4 rounded-full mb-4">
            <Plus className="size-8 text-primary" />
          </div>
          <h3 className="text-lg font-semibold">No trips planned yet</h3>
          <p className="text-muted-foreground mb-4 max-w-sm">
            Start your adventure by creating your first trip itinerary.
          </p>
          <Button asChild>
            <Link href="/trips/create">Create Trip</Link>
          </Button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {trips.map((trip) => (
            <TripCard key={trip.id} trip={trip} />
          ))}
        </div>
      )}
    </div>
  );
}
