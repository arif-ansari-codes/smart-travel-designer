import logging
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_trip_plan(data: dict) -> str:
    """
    Generate a complete trip plan using OpenAI.
    The `data` dictionary must contain:
    - city, days, forecast, attractions, restaurants, hotel_cost, flight_cost, events, alerts, etc.
    """
    prompt = f"""
You are a helpful AI Travel Assistant. Create a detailed travel plan based on the user's input.

City: {data['city']}
Days: {data['days']}
Top Attractions: {', '.join(data['attractions']) or 'Not found'}
Top Restaurants: {', '.join(data['restaurants']) or 'Not found'}
Weather Forecast: {data['forecast']}
Hotel Cost Estimate: {data['hotel_cost']} USD
Flight Cost Estimate: {data['flight_cost']} USD
Currency: {data['currency']}
Exchange Rate (to local): {data['exchange_rate']}
Total Estimated Cost: {data['total_cost']} {data['currency']}
Events: {', '.join(data.get('events', [])) or 'None'}
Safety Alerts: {', '.join(data.get('alerts', [])) or 'None'}

Instructions:
- Give a day-by-day plan.
- Recommend specific places and local food.
- Suggest ideal times for sightseeing.
- Be concise but vivid.
- End with a travel tip or safety note.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert travel planner."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()
