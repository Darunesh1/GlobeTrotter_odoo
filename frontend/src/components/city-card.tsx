"use client";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MapPin, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export interface City {
  id: string;
  name: string;
  country: string;
  image?: string;
  description?: string;
  cost_index?: number; // 1-5 scale?
}

export function CityCard({ city }: { city: City }) {
  return (
    <Card className="hover:shadow-lg transition-all duration-300 group overflow-hidden border-primary/10">
      <div className="aspect-[4/3] bg-muted relative overflow-hidden">
        {city.image ? (
          <img
            src={city.image}
            alt={city.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-muted-foreground bg-primary/5">
            <MapPin className="size-10 text-primary/40" />
          </div>
        )}
        <div className="absolute top-2 right-2 bg-black/60 text-white px-2 py-1 rounded text-xs font-medium">
          {city.country}
        </div>
      </div>
      <CardHeader className="pb-2">
        <CardTitle className="truncate font-bold text-lg">
          {city.name}
        </CardTitle>
      </CardHeader>
      <CardContent className="pb-2 text-sm text-muted-foreground">
        <p className="line-clamp-2">
          {city.description || `Explore the wonders of ${city.name}.`}
        </p>
      </CardContent>
      <CardFooter>
        <Button
          variant="secondary"
          className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
          asChild
        >
          <Link href={`/search?city=${city.id}`}>
            Explore
            <ArrowRight className="ml-2 size-4" />
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
