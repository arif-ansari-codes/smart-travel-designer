import logging
import requests
from app.core.config import settings

logger = logging.getLogger(__name__)


class WeatherServiceError(Exception):
    pass


def fetch_weather(city: str, days: int) -> list:
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": settings.OPENWEATHER_KEY,
        "units": "metric",
        "cnt": days * 8,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Weather API timed out for city: %s", city)
        raise WeatherServiceError(f"Weather service timed out for '{city}'")
    except requests.exceptions.HTTPError as e:
        logger.error(
            "Weather API HTTP error: %s — %s",
            e.response.status_code,
            e.response.text,
        )
        raise WeatherServiceError(
            f"Weather service error for '{city}': {e.response.status_code}"
        )
    except requests.exceptions.RequestException as e:
        logger.error("Weather API request failed: %s", e)
        raise WeatherServiceError("Weather service unavailable")

    data = response.json()
    daily: dict = {}
    for item in data.get("list", []):
        date = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        daily.setdefault(date, []).append(temp)

    return [
        {
            "date": d,
            "min": round(min(temps), 2),
            "max": round(max(temps), 2),
            "avg": round(sum(temps) / len(temps), 2),
        }
        for d, temps in daily.items()
    ]
