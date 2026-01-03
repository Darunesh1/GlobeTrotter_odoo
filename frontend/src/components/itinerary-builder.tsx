"use client";

import React, { useState } from "react";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragOverlay,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { GripVertical, Plus, MapPin, Clock } from "lucide-react";

// --- Types ---
interface Activity {
  id: string;
  title: string;
  duration?: string;
  cost?: number;
}

interface Stop {
  id: string;
  city: string;
  activities: Activity[];
}

// --- Sortable Item Component ---
function SortableStop({ stop }: { stop: Stop }) {
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id: stop.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} style={style} className="mb-4">
      <Card className="border-primary/20">
        <CardHeader className="flex flex-row items-center space-y-0 py-3 bg-muted/50 rounded-t-lg">
          <div
            {...attributes}
            {...listeners}
            className="cursor-grab mr-2 text-muted-foreground hover:text-foreground"
          >
            <GripVertical className="size-5" />
          </div>
          <CardTitle className="text-base font-semibold flex items-center gap-2">
            <MapPin className="size-4 text-primary" />
            {stop.city}
          </CardTitle>
          <Button
            variant="ghost"
            size="sm"
            className="ml-auto text-muted-foreground hover:text-destructive"
          >
            Remove
          </Button>
        </CardHeader>
        <CardContent className="pt-4 space-y-2">
          {stop.activities.length === 0 ? (
            <div className="text-sm text-center text-muted-foreground border border-dashed rounded py-4">
              No activities yet.
              <Button variant="link" size="sm" className="h-auto p-0 ml-1">
                Add one
              </Button>
            </div>
          ) : (
            stop.activities.map((activity) => (
              <div
                key={activity.id}
                className="flex items-center justify-between p-2 bg-background border rounded text-sm"
              >
                <span>{activity.title}</span>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  {activity.duration && (
                    <span className="flex items-center gap-1">
                      <Clock className="size-3" />
                      {activity.duration}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
          <Button variant="outline" size="sm" className="w-full mt-2">
            <Plus className="mr-2 size-3" /> Add Activity
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

// --- Main Builder Component ---
export default function ItineraryBuilder() {
  // Mock Data
  const [stops, setStops] = useState<Stop[]>([
    {
      id: "1",
      city: "Paris, France",
      activities: [
        { id: "a1", title: "Eiffel Tower", duration: "2h" },
        { id: "a2", title: "Louvre Museum", duration: "3h" },
      ],
    },
    { id: "2", city: "London, UK", activities: [] },
  ]);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragEnd(event: any) {
    const { active, over } = event;

    if (active.id !== over.id) {
      setStops((items) => {
        const oldIndex = items.findIndex((i) => i.id === active.id);
        const newIndex = items.findIndex((i) => i.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Itinerary Builder</h2>
        <Button>
          <Plus className="mr-2 size-4" /> Add Stop
        </Button>
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={stops.map((s) => s.id)}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-4">
            {stops.map((stop) => (
              <SortableStop key={stop.id} stop={stop} />
            ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );
}
