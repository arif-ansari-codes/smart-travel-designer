export interface WeatherDay {
  date: string;
  min: number;
  max: number;
  avg: number;
}

export interface EstimatedCosts {
  per_day: number;
  total: number;
  currency: string;
}

export interface TripPlanRequest {
  username: string;
  home_country: string;
  currency: string;
  trip_country: string;
  city: string;
  days: number;
}

export interface TripPlanResponse {
  summary: string;
  photos: string[];
  weather: WeatherDay[];
  exchange_rate: string;
  estimated_costs: EstimatedCosts;
}
