"use client";

import Image from "next/image";
import ReactMarkdown from "react-markdown";
import type { TripPlanResponse } from "@/types/api";
import { WeatherCard } from "@/components/WeatherCard";
import { CostCard } from "@/components/CostCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface TripResultsProps {
  data: TripPlanResponse;
  days: number;
}

export function TripResults({ data, days }: TripResultsProps) {
  return (
    <div className="space-y-6">
      {/* Trip Itinerary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl">
            Trip Itinerary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm max-w-none text-foreground leading-relaxed">
            <ReactMarkdown>{data.summary}</ReactMarkdown>
          </div>
        </CardContent>
      </Card>

      {/* Photos */}
      {data.photos.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Destination Photos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {data.photos.map((url, idx) => (
                <div key={idx} className="relative w-full h-48 rounded-lg overflow-hidden shadow-md">
                  <Image
                    src={url}
                    alt={`Destination photo ${idx + 1}`}
                    fill
                    className="object-cover"
                    sizes="(max-width: 640px) 100vw, 33vw"
                    unoptimized
                  />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Cost + Exchange Rate */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <CostCard costs={data.estimated_costs} days={days} />

        <Card>
          <CardHeader>
            <CardTitle>Exchange Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{data.exchange_rate}</p>
          </CardContent>
        </Card>
      </div>

      {/* Weather Forecast */}
      {data.weather.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Weather Forecast</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              {data.weather.map((day) => (
                <WeatherCard key={day.date} day={day} />
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
