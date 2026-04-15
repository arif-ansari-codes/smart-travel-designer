import type { EstimatedCosts } from "@/types/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CostCardProps {
  costs: EstimatedCosts;
  days: number;
}

export function CostCard({ costs, days }: CostCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Estimated Cost</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <p className="text-lg font-semibold">
          {costs.per_day.toLocaleString()} {costs.currency}{" "}
          <span className="text-sm font-normal text-muted-foreground">/ day</span>
        </p>
        <p className="text-muted-foreground text-sm">
          Total for {days} {days === 1 ? "day" : "days"}:{" "}
          <span className="font-medium text-foreground">
            {costs.total.toLocaleString()} {costs.currency}
          </span>
        </p>
      </CardContent>
    </Card>
  );
}
