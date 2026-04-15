import logging
import requests
from app.core.config import settings

logger = logging.getLogger(__name__)


class ExchangeServiceError(Exception):
    pass


def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/{from_currency.upper()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Exchange rate API timed out")
        raise ExchangeServiceError("Exchange rate service timed out")
    except requests.exceptions.RequestException as e:
        logger.error("Exchange rate API request failed: %s", e)
        raise ExchangeServiceError(f"Exchange rate service error: {e}")

    data = response.json()
    rate = data.get("conversion_rates", {}).get(to_currency.upper())

    if rate is None:
        logger.warning("Exchange rate not found for currency: %s", to_currency)
        raise ExchangeServiceError(f"Exchange rate not found for '{to_currency}'")

    return f"1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"
