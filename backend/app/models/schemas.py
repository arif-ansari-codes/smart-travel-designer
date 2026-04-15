from pydantic import BaseModel
from typing import List

class WeatherRequest(BaseModel):
    city: str
    days: int

# app/models/schemas.py


class ForecastEntry(BaseModel):
    date: str
    min: float
    max: float
    avg: float

class TripPlanRequest(BaseModel):
    city: str
    days: int
    attractions: List[str]
    restaurants: List[str]
    forecast: List[ForecastEntry]
    hotel_cost: float
    flight_cost: float
    exchange_rate: float
    total_cost: float
    events: List[str]
    alerts: List[str]
    currency: str
    photos: List[str] = []

class TripPlanResponse(BaseModel):
    summary: str
    photos: List[str]
