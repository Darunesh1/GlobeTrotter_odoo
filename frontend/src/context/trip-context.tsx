"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
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

export interface Stop {
  id: number;
  trip_id: number;
  city_id: number;
  order: number;
  start_date: string;
  end_date: string;
  notes?: string;
  transport_cost?: number;
  city: {
    id: number;
    name: string;
    country: string;
    image_url?: string;
    latitude?: number;
    longitude?: number;
  };
  activities: any[];
}

interface TripContextType {
  trip: Trip | null;
  stops: Stop[];
  isLoading: boolean;
  refreshTrip: () => Promise<void>;
  updateTrip: (data: Partial<Trip>) => Promise<void>;
  deleteTrip: () => Promise<void>;
  addStop: (data: any) => Promise<void>;
  removeStop: (stopId: number) => Promise<void>;
}

const TripContext = createContext<TripContextType | undefined>(undefined);

export function TripProvider({ children }: { children: React.ReactNode }) {
  const [trip, setTrip] = useState<Trip | null>(null);
  const [stops, setStops] = useState<Stop[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const refreshTrip = async () => {
    try {
      setIsLoading(true);
      const { data: tripData } = await api.get(`/trips/${id}`);
      setTrip(tripData);

      const { data: stopsData } = await api.get(`/trips/${id}/stops`);
      setStops(stopsData);
    } catch (error) {
      console.error("Failed to fetch trip", error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateTrip = async (data: Partial<Trip>) => {
    try {
      const { data: updatedTrip } = await api.put(`/trips/${id}`, data);
      setTrip(updatedTrip);
    } catch (error) {
      console.error("Failed to update trip", error);
      throw error;
    }
  };

  const deleteTrip = async () => {
    try {
      await api.delete(`/trips/${id}`);
      router.push("/dashboard");
    } catch (error) {
      console.error("Failed to delete trip", error);
      throw error;
    }
  };

  const addStop = async (stopData: any) => {
    try {
      await api.post(`/trips/${id}/stops`, stopData);
      await refreshTrip();
    } catch (error) {
      console.error("Failed to add stop", error);
      throw error;
    }
  };

  const removeStop = async (stopId: number) => {
    try {
      await api.delete(`/stops/${stopId}`);
      setStops((prev) => prev.filter((s) => s.id !== stopId));
    } catch (error) {
      console.error("Failed to delete stop", error);
      throw error;
    }
  };

  useEffect(() => {
    if (id) {
      refreshTrip();
    }
  }, [id]);

  return (
    <TripContext.Provider
      value={{
        trip,
        stops,
        isLoading,
        refreshTrip,
        updateTrip,
        deleteTrip,
        addStop,
        removeStop,
      }}
    >
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
