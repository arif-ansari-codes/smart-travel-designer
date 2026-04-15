import logging
import requests
from typing import List, Dict
from app.core.config import settings

logger = logging.getLogger(__name__)

HEADERS = {"accept": "application/json"}


def get_location_id_and_latlong(city: str):
    search_url = "https://api.content.tripadvisor.com/api/v1/location/search"
    search_params = {
        "searchQuery": city,
        "language": "en",
        "key": settings.TRIPADVISOR_KEY,
        "category": "geos",
    }
    search_resp = requests.get(search_url, headers=HEADERS, params=search_params, timeout=10)
    search_resp.raise_for_status()
    search_data = search_resp.json()

    try:
        location_id = search_data["data"][0]["location_id"]
    except (KeyError, IndexError):
        logger.warning("TripAdvisor location ID not found for city: %s", city)
        return None, None

    details_url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
    details_params = {"key": settings.TRIPADVISOR_KEY, "language": "en"}
    details_resp = requests.get(details_url, headers=HEADERS, params=details_params, timeout=10)
    details_resp.raise_for_status()
    details_data = details_resp.json()

    try:
        lat = details_data["latitude"]
        lon = details_data["longitude"]
        return location_id, f"{lat},{lon}"
    except KeyError:
        logger.warning("Failed to extract lat/long for location_id: %s", location_id)
        return location_id, None


def get_nearby(latlong: str, category: str) -> List[str]:
    url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search"
    params = {
        "key": settings.TRIPADVISOR_KEY,
        "language": "en",
        "latLong": latlong,
        "category": category,
        "radius": "5",
        "radiusUnit": "km",
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [item.get("name") for item in data.get("data", []) if item.get("name")][:6]


def get_photos(location_id: str) -> List[str]:
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/photos"
    params = {
        "key": settings.TRIPADVISOR_KEY,
        "language": "en",
        "limit": 20,
        "source": "Traveler",
    }
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    photos = []
    for item in data.get("data", []):
        caption = item.get("caption", "").lower()
        if "restaurant" in caption or "food" in caption:
            continue
        photo_url = item.get("images", {}).get("original", {}).get("url")
        if photo_url:
            photos.append(photo_url)
        if len(photos) >= 6:
            break
    return photos


def get_tripadvisor_data(city: str) -> Dict:
    logger.info("Fetching TripAdvisor data for: %s", city)

    try:
        location_id, latlong = get_location_id_and_latlong(city)
    except Exception as e:
        logger.error("TripAdvisor location lookup failed for '%s': %s", city, e)
        return {"attractions": [], "restaurants": [], "photos": []}

    if not location_id or not latlong:
        return {"attractions": [], "restaurants": [], "photos": []}

    attractions, restaurants, photos = [], [], []

    try:
        attractions = get_nearby(latlong, "attractions")
    except Exception as e:
        logger.warning("Failed to fetch attractions for '%s': %s", city, e)

    try:
        restaurants = get_nearby(latlong, "restaurants")
    except Exception as e:
        logger.warning("Failed to fetch restaurants for '%s': %s", city, e)

    try:
        photos = get_photos(location_id)
    except Exception as e:
        logger.warning("Failed to fetch photos for location_id '%s': %s", location_id, e)

    return {"attractions": attractions, "restaurants": restaurants, "photos": photos}
