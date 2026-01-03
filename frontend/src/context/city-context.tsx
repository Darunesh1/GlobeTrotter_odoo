"use client";

import React, { createContext, useContext, useState } from "react";
import api from "@/lib/api";

export interface City {
  id: number;
  name: string;
  country: string;
  region?: string;
  description?: string;
  image_url?: string;
  avg_cost_per_day?: number;
  popularity_score?: number;
  latitude?: number;
  longitude?: number;
}

interface CityContextType {
  cities: City[];
  popularCities: City[];
  isLoading: boolean;
  searchCities: (query: string) => Promise<void>;
  getPopularCities: () => Promise<void>;
  getCity: (id: number) => Promise<City>;
}

const CityContext = createContext<CityContextType | undefined>(undefined);

export function CityProvider({ children }: { children: React.ReactNode }) {
  const [cities, setCities] = useState<City[]>([]);
  const [popularCities, setPopularCities] = useState<City[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const searchCities = async (query: string) => {
    setIsLoading(true);
    try {
      const { data } = await api.get(`/cities/?search=${query}`);
      setCities(data);
    } catch (error) {
      console.error("Failed to search cities", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getPopularCities = async () => {
    try {
      const { data } = await api.get("/cities/popular");
      setPopularCities(data);
    } catch (error) {
      console.error("Failed to fetch popular cities", error);
    }
  };

  const getCity = async (id: number) => {
    try {
      const { data } = await api.get(`/cities/${id}`);
      return data;
    } catch (error) {
      console.error("Failed to fetch city", error);
      throw error;
    }
  };

  return (
    <CityContext.Provider
      value={{
        cities,
        popularCities,
        isLoading,
        searchCities,
        getPopularCities,
        getCity,
      }}
    >
      {children}
    </CityContext.Provider>
  );
}

export const useCity = () => {
  const context = useContext(CityContext);
  if (!context) {
    throw new Error("useCity must be used within a CityProvider");
  }
  return context;
};
