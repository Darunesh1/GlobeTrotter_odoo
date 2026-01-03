"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { Trip } from "@/components/trip-card";

interface TripContextType {
  trip: Trip | null;
  isLoading: boolean;
  refreshTrip: () => Promise<void>;
}

const TripContext = createContext<TripContextType | undefined>(undefined);

export function TripProvider({ children }: { children: React.ReactNode }) {
  const [trip, setTrip] = useState<Trip | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const params = useParams();
  const id = params.id as string;

  const refreshTrip = async () => {
    try {
      const { data } = await api.get(`/trips/${id}`);
      setTrip(data);
    } catch (error) {
      console.error("Failed to fetch trip", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      refreshTrip();
    }
  }, [id]);

  return (
    <TripContext.Provider value={{ trip, isLoading, refreshTrip }}>
      {children}
    </TripContext.Provider>
  );
}

export const useTrip = () => {
  const context = useContext(TripContext);
  if (!context) {
    throw new Error("useTrip must be used within a TripProvider");
  }
  return context;
};
