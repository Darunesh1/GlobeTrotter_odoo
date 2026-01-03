"use client";

import { TripProvider, useTrip } from "@/context/trip-context";
import {
  Loader2,
  MapPin,
  Calendar,
  DollarSign,
  Settings,
  Share2,
  ArrowLeft,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function TripLayoutContent({ children }: { children: React.ReactNode }) {
  const { trip, isLoading } = useTrip();
  const pathname = usePathname();

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <Loader2 className="animate-spin size-8 text-primary" />
      </div>
    );
  }

  if (!trip) {
    return <div className="p-8 text-center">Trip not found</div>;
  }

  const tabs = [
    { name: "Itinerary", href: `/trips/${trip.id}`, icon: MapPin },
    { name: "Budget", href: `/trips/${trip.id}/budget`, icon: DollarSign },
    { name: "Calendar", href: `/trips/${trip.id}/calendar`, icon: Calendar },
    { name: "Sharing", href: `/trips/${trip.id}/share`, icon: Share2 },
  ];

  return (
    <div className="space-y-6">
      {/* Header / Cover */}
      <div className="relative h-64 md:h-80 w-full overflow-hidden rounded-lg shadow-md bg-muted group">
        {trip.cover_photo && (
          <img
            src={trip.cover_photo}
            alt={trip.name}
            className="w-full h-full object-cover"
          />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent flex flex-col justify-end p-6 text-white">
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-4 left-4 text-white hover:bg-white/20"
            asChild
          >
            <Link href="/trips">
              <ArrowLeft />
            </Link>
          </Button>
          <h1 className="text-3xl md:text-5xl font-bold mb-2">{trip.name}</h1>
          <div className="flex items-center gap-4 text-sm md:text-base opacity-90">
            <span>
              {new Date(trip.start_date).toDateString()} -{" "}
              {new Date(trip.end_date).toDateString()}
            </span>
            {trip.description && (
              <span className="hidden md:inline">• {trip.description}</span>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b">
        <nav className="flex space-x-4 md:space-x-8 overflow-x-auto pb-1">
          {tabs.map((tab) => {
            const isActive = pathname === tab.href;
            return (
              <Link
                key={tab.name}
                href={tab.href}
                className={cn(
                  "flex items-center gap-2 px-1 py-4 text-sm font-medium border-b-2 transition-colors whitespace-nowrap",
                  isActive
                    ? "border-primary text-primary"
                    : "border-transparent text-muted-foreground hover:text-foreground hover:border-muted"
                )}
              >
                <tab.icon className="size-4" />
                {tab.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Sub-page Content */}
      <div className="min-h-[500px]">{children}</div>
    </div>
  );
}

export default function TripLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <TripProvider>
      <TripLayoutContent>{children}</TripLayoutContent>
    </TripProvider>
  );
}
