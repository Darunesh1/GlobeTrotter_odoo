"use client";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Calendar, MapPin, MoreHorizontal } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { format } from "date-fns";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export interface Trip {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  cover_photo?: string;
  description?: string;
  city_count?: number;
}

export function TripCard({ trip }: { trip: Trip }) {
  return (
    <Card className="hover:shadow-lg transition-all duration-300 group overflow-hidden border-primary/10">
      <div className="aspect-video bg-muted relative overflow-hidden">
        {trip.cover_photo ? (
          <img
            src={trip.cover_photo}
            alt={trip.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-muted-foreground bg-primary/5 group-hover:bg-primary/10 transition-colors">
            <MapPin className="size-10 text-primary/40" />
          </div>
        )}
      </div>
      <CardHeader className="pb-2 relative">
        <div className="flex justify-between items-start">
          <CardTitle className="truncate text-lg font-bold">
            {trip.name}
          </CardTitle>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 -mr-2 -mt-2"
              >
                <MoreHorizontal className="size-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>Edit Details</DropdownMenuItem>
              <DropdownMenuItem className="text-destructive">
                Delete Trip
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      <CardContent className="pb-2 text-sm text-muted-foreground space-y-2">
        <div className="flex items-center gap-2">
          <Calendar className="size-4 text-primary" />
          <span>
            {format(new Date(trip.start_date), "MMM d, yyyy")} -{" "}
            {format(new Date(trip.end_date), "MMM d, yyyy")}
          </span>
        </div>
        {trip.description && (
          <p className="line-clamp-2 text-xs opacity-80">{trip.description}</p>
        )}
      </CardContent>
      <CardFooter className="pt-2">
        <Button asChild className="w-full shadow-md hover:shadow-primary/20">
          <Link href={`/trips/${trip.id}`}>View Itinerary</Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
