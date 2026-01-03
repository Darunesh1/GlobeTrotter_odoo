"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import api from "@/lib/api";

export interface Trip {
  id: number;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  cover_photo?: string;
  user_id: number;
  is_public: number;
  share_token?: string;
  created_at: string;
  updated_at: string;
}

interface TripsContextType {
  trips: Trip[];
  isLoading: boolean;
  fetchTrips: () => Promise<void>;
  createTrip: (data: any) => Promise<Trip>;
}

const TripsContext = createContext<TripsContextType | undefined>(undefined);

export function TripsProvider({ children }: { children: React.ReactNode }) {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchTrips = async () => {
    try {
      const { data } = await api.get("/trips/");
      setTrips(data);
    } catch (error) {
      console.error("Failed to fetch trips", error);
    } finally {
      setIsLoading(false);
    }
  };

  const createTrip = async (data: any) => {
    try {
      const { data: newTrip } = await api.post("/trips/", data);
      setTrips((prev) => [...prev, newTrip]);
      return newTrip;
    } catch (error) {
      console.error("Failed to create trip", error);
      throw error;
    }
  };

  useEffect(() => {
    fetchTrips();
  }, []);

  return (
    <TripsContext.Provider value={{ trips, isLoading, fetchTrips, createTrip }}>
      {children}
    </TripsContext.Provider>
  );
}

export const useTrips = () => {
  const context = useContext(TripsContext);
  if (!context) {
    throw new Error("useTrips must be used within a TripsProvider");
  }
  return context;
};
