import { z } from "zod";

export const tripFormSchema = z.object({
  username: z.string().min(1, "Name is required").max(100),
  home_country: z.string().min(1, "Home country is required"),
  currency: z
    .string()
    .length(3, "Must be a 3-letter currency code (e.g. USD, INR)")
    .transform((v) => v.toUpperCase()),
  trip_country: z.string().min(1, "Destination country is required"),
  city: z.string().min(1, "City is required"),
  days: z.coerce
    .number({ invalid_type_error: "Days must be a number" })
    .int("Days must be a whole number")
    .min(1, "Minimum 1 day")
    .max(30, "Maximum 30 days"),
});

export type TripFormValues = z.infer<typeof tripFormSchema>;
