import axios, { AxiosError } from "axios";
import type { TripPlanRequest, TripPlanResponse } from "@/types/api";

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  timeout: 90000,
  headers: { "Content-Type": "application/json" },
});

export class TripApiError extends Error {
  constructor(
    public readonly statusCode: number | undefined,
    message: string
  ) {
    super(message);
    this.name = "TripApiError";
  }
}

export async function fetchTripPlan(data: TripPlanRequest): Promise<TripPlanResponse> {
  try {
    const response = await apiClient.post<TripPlanResponse>("/trip-plan/", data);
    return response.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      const status = error.response?.status;
      const detail = error.response?.data?.detail ?? error.message;
      throw new TripApiError(status, `${detail}`);
    }
    throw new TripApiError(undefined, "Network error: could not reach the server");
  }
}
