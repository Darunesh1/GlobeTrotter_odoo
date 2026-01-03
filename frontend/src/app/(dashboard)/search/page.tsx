"use client";

import { useState, useEffect } from "react";
import { Search, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CityCard, City } from "@/components/city-card";
import api from "@/lib/api";
import { toast } from "sonner";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<City[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const handleSearch = async () => {
    setIsLoading(true);
    try {
      // Mock search or actual API
      const { data } = await api.get("/cities", { params: { search: query } });
      setResults(data);
    } catch (error) {
      console.error(error);
      // Fallback for demo if API fails
      setResults([
        {
          id: "1",
          name: "Paris",
          country: "France",
          description: "The City of Light.",
          image:
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&q=80&w=1000",
        },
        {
          id: "2",
          name: "Tokyo",
          country: "Japan",
          description: "Neon lights and ancient temples.",
          image:
            "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&q=80&w=1000",
        },
        {
          id: "3",
          name: "New York",
          country: "USA",
          description: "The city that never sleeps.",
          image:
            "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&q=80&w=1000",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Auto search on load
  useEffect(() => {
    handleSearch();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <h2 className="text-3xl font-bold tracking-tight text-primary">
          Discover Destinations
        </h2>
        <div className="relative w-full md:w-[400px]">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search for cities, countries..."
            className="pl-8 bg-background"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
        </div>
      </div>

      <Tabs defaultValue="cities" className="w-full">
        <TabsList>
          <TabsTrigger value="cities">Cities</TabsTrigger>
          <TabsTrigger value="activities">Activities</TabsTrigger>
        </TabsList>
        <TabsContent value="cities" className="mt-6">
          {isLoading ? (
            <div className="flex justify-center p-8">
              <Loader2 className="animate-spin text-primary" />
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {results.map((city) => (
                <CityCard key={city.id} city={city} />
              ))}
            </div>
          )}
        </TabsContent>
        <TabsContent value="activities">
          <div className="p-12 text-center text-muted-foreground border rounded-lg border-dashed">
            Activity search coming soon.
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
