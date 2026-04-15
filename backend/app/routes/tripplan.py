import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI, OpenAIError

from app.core.config import settings
from app.services.weather_service import fetch_weather, WeatherServiceError
from app.services.tripadvisor import get_tripadvisor_data
from app.services.exchange import get_exchange_rate, ExchangeServiceError
from app.services.cost_extractor import extract_average_cost
from app.services.utils import get_currency_for_country

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)
router = APIRouter()


class TripPlanRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    home_country: str = Field(min_length=1, max_length=100)
    currency: str = Field(min_length=3, max_length=3)
    trip_country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    days: int = Field(ge=1, le=30)

    @field_validator("currency")
    @classmethod
    def currency_uppercase(cls, v: str) -> str:
        return v.upper()


@router.post("/trip-plan/")
def trip_plan(req: TripPlanRequest):
    logger.info(
        "Trip plan request: user=%s city=%s days=%d", req.username, req.city, req.days
    )

    # 1. Fetch weather
    try:
        weather = fetch_weather(req.city, req.days)
    except WeatherServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # 2. Fetch TripAdvisor data (gracefully degrades on partial failure)
    trip_data = get_tripadvisor_data(req.city)

    # 3. Get destination currency and exchange rate
    trip_currency = get_currency_for_country(req.trip_country)
    try:
        rate_info = get_exchange_rate(req.currency, trip_currency)
    except ExchangeServiceError as e:
        logger.warning("Exchange rate fetch failed, continuing without it: %s", e)
        rate_info = f"Exchange rate unavailable for {req.currency} → {trip_currency}"

    # 4. Build prompt
    prompt = f"""
You are a helpful travel planner AI. Create a {req.days}-day travel plan for {req.username} who lives in {req.home_country} and wants to visit {req.city}.
The user's currency is {req.currency} and the trip country currency is {trip_currency}.

Include:
- Suggested attractions: {trip_data['attractions']}
- Suggested restaurants: {trip_data['restaurants']}
- Weather: {weather}
- Exchange Rate: {rate_info}

Give 1 paragraph per day. Include rough cost for each day in the user's local currency ({req.currency}). End with a closing travel tip.
"""

    # 5. Call OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            timeout=60,
        )
    except OpenAIError as e:
        logger.error("OpenAI API error: %s", e)
        raise HTTPException(status_code=502, detail="AI service temporarily unavailable")

    summary = response.choices[0].message.content

    # 6. Extract cost
    per_day = extract_average_cost(summary, req.currency)
    total = per_day * req.days

    logger.info(
        "Trip plan generated: user=%s city=%s cost_per_day=%d", req.username, req.city, per_day
    )

    return {
        "summary": summary,
        "photos": trip_data["photos"][:3],
        "weather": weather,
        "exchange_rate": rate_info,
        "estimated_costs": {
            "per_day": per_day,
            "total": total,
            "currency": req.currency,
        },
    }
