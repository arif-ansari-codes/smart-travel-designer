"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { tripFormSchema, type TripFormValues } from "@/lib/tripSchema";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface TripFormProps {
  onSubmit: (data: TripFormValues) => Promise<void>;
  isLoading: boolean;
}

export function TripForm({ onSubmit, isLoading }: TripFormProps) {
  const form = useForm<TripFormValues>({
    resolver: zodResolver(tripFormSchema),
    defaultValues: {
      username: "",
      home_country: "",
      currency: "",
      trip_country: "",
      city: "",
      days: 1,
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Name</FormLabel>
                <FormControl>
                  <Input placeholder="Your name" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="home_country"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Home Country</FormLabel>
                <FormControl>
                  <Input placeholder="e.g. India" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="currency"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Currency (e.g. USD, INR)</FormLabel>
                <FormControl>
                  <Input placeholder="INR" maxLength={3} {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="trip_country"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Trip Country</FormLabel>
                <FormControl>
                  <Input placeholder="e.g. United Kingdom" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="city"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Trip City</FormLabel>
                <FormControl>
                  <Input placeholder="e.g. London" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="days"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Number of Days</FormLabel>
                <FormControl>
                  <Input type="number" min={1} max={30} placeholder="4" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <Button type="submit" disabled={isLoading} className="w-full md:w-auto">
          {isLoading ? "Generating..." : "Generate Trip Plan"}
        </Button>
      </form>
    </Form>
  );
}
