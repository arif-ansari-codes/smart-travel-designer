import type { WeatherDay } from "@/types/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface WeatherCardProps {
  day: WeatherDay;
}

export function WeatherCard({ day }: WeatherCardProps) {
  return (
    <Card className="text-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold">{day.date}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-1 text-muted-foreground">
        <p>Avg: {day.avg}°C</p>
        <p>Min: {day.min}°C</p>
        <p>Max: {day.max}°C</p>
      </CardContent>
    </Card>
  );
}
