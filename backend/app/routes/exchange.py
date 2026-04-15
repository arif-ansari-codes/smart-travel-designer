import logging
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class ExchangeRateRequest(BaseModel):
    currency: str


class ExchangeRateResponse(BaseModel):
    currency: str
    rate: float


@router.post("/exchange-rate/", response_model=ExchangeRateResponse)
def get_exchange_rate_route(req: ExchangeRateRequest):
    if not settings.EXCHANGE_RATE_API_KEY:
        raise HTTPException(status_code=500, detail="Exchange rate API key not configured")

    url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/USD"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("Exchange rate API failed: %s", e)
        raise HTTPException(status_code=502, detail="Exchange rate service unavailable")

    data = resp.json()
    rate = data.get("conversion_rates", {}).get(req.currency.upper())

    if rate is None:
        raise HTTPException(status_code=404, detail=f"Currency '{req.currency}' not found")

    return ExchangeRateResponse(currency=req.currency.upper(), rate=rate)
