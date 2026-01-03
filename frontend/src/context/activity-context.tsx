"use client";

import React, { createContext, useContext, useState } from "react";
import api from "@/lib/api";

export interface Activity {
  id: number;
  city_id: number;
  name: string;
  category?: string;
  description?: string;
  estimated_cost?: number;
  duration_hours?: number;
  image_url?: string;
}

interface ActivityContextType {
  activities: Activity[];
  isLoading: boolean;
  searchActivities: (cityId?: number, category?: string) => Promise<void>;
  addActivityToStop: (stopId: number, activityId: number, actualCost?: number) => Promise<void>;
  removeActivityFromStop: (stopId: number, activityId: number) => Promise<void>;
}

const ActivityContext = createContext<ActivityContextType | undefined>(undefined);

export function ActivityProvider({ children }: { children: React.ReactNode }) {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const searchActivities = async (cityId?: number, category?: string) => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      if (cityId) params.append("city_id", cityId.toString());
      if (category) params.append("category", category);
      
      const { data } = await api.get(`/activities/?${params.toString()}`);
      setActivities(data);
    } catch (error) {
      console.error("Failed to search activities", error);
    } finally {
      setIsLoading(false);
    }
  };

  const addActivityToStop = async (stopId: number, activityId: number, actualCost?: number) => {
    try {
      await api.post(`/activities/stop/${stopId}`, {
        activity_id: activityId,
        actual_cost: actualCost
      });
    } catch (error) {
      console.error("Failed to add activity to stop", error);
      throw error;
    }
  };

  const removeActivityFromStop = async (stopId: number, activityId: number) => {
    try {
      await api.delete(`/activities/stop/${stopId}/${activityId}`);
    } catch (error) {
      console.error("Failed to remove activity from stop", error);
      throw error;
    }
  };

  return (
    <ActivityContext.Provider
      value={{
        activities,
        isLoading,
        searchActivities,
        addActivityToStop,
        removeActivityFromStop,
      }}
    >
      {children}
    </ActivityContext.Provider>
  );
}

export const useActivity = () => {
  const context = useContext(ActivityContext);
  if (!context) {
    throw new Error("useActivity must be used within an ActivityProvider");
  }
  return context;
};
