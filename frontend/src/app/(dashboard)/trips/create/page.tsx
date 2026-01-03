"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Map, Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { DateRange } from "react-day-picker";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { DatePickerWithRange } from "@/components/date-range-picker";
import { toast } from "sonner";
import api from "@/lib/api";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const formSchema = z.object({
  name: z
    .string()
    .min(2, { message: "Trip name must be at least 2 characters." }),
  description: z.string().optional(),
  // Dates are handled separately via state to sync with DateRangePicker
  // But we can add custom validation if needed
});

export default function CreateTripPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [date, setDate] = useState<DateRange | undefined>();
  const router = useRouter();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    if (!date?.from || !date?.to) {
      toast.error("Dates required", {
        description: "Please select a start and end date for your trip.",
      });
      return;
    }

    setIsLoading(true);
    try {
      const payload = {
        ...values,
        start_date: date.from.toISOString(),
        end_date: date.to.toISOString(),
        cover_photo:
          "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2021&auto=format&fit=crop", // Default placeholder
      };

      await api.post("/trips", payload);

      toast.success("Trip created!", {
        description: "Your new adventure awaits.",
      });

      router.push("/trips");
    } catch (error: any) {
      console.error(error);
      toast.error("Failed to create trip", {
        description: error.message || "Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" asChild>
          <Link href="/trips">
            <ArrowLeft className="size-4" />
          </Link>
        </Button>
        <h2 className="text-3xl font-bold tracking-tight text-primary">
          Plan a New Trip
        </h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Trip Details</CardTitle>
          <CardDescription>
            Give your trip a name and choose your travel dates.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Trip Name</FormLabel>
                    <FormControl>
                      <Input placeholder="e.g. Summer in Italy" {...field} />
                    </FormControl>
                    <FormDescription>
                      A memorable name for your journey.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormItem>
                <FormLabel>Travel Dates</FormLabel>
                <FormControl>
                  <DatePickerWithRange date={date} setDate={setDate} />
                </FormControl>
                <FormDescription>
                  Select the start and end dates.
                </FormDescription>
              </FormItem>

              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description (Optional)</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="What's the goal of this trip?"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Map className="mr-2 h-4 w-4" />
                )}
                Create Trip
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
