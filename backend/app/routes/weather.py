from fastapi import APIRouter
from app.models.schemas import WeatherRequest
from app.services.weather_service import fetch_weather

router = APIRouter()

@router.post("/forecast")
def get_forecast(request: WeatherRequest):
    data = fetch_weather(request.city, request.days)
    return {"forecast": data}
