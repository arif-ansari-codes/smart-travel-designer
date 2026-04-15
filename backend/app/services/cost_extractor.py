import re

CURRENCY_DAILY_DEFAULTS = {
    "USD": 150,
    "EUR": 140,
    "GBP": 120,
    "JPY": 18000,
    "INR": 4000,
    "AUD": 220,
    "CAD": 200,
    "SGD": 200,
    "AED": 550,
    "ZAR": 2500,
    "CNY": 1000,
    "BRL": 750,
    "MXN": 2500,
    "THB": 5000,
    "TRY": 4000,
}
DEFAULT_DAILY_USD_EQUIVALENT = 150


def extract_average_cost(summary: str, currency_code: str) -> int:
    code = currency_code.upper()
    escaped = re.escape(code)

    pattern = rf"(?:around|approximately|estimated|roughly)?\s*(?:{escaped}\s*([\d,]+)|([\d,]+)\s*{escaped})"
    matches = re.findall(pattern, summary)

    if not matches:
        return CURRENCY_DAILY_DEFAULTS.get(code, DEFAULT_DAILY_USD_EQUIVALENT)

    costs = [int(cost.replace(",", "")) for pair in matches for cost in pair if cost]
    return sum(costs) // len(costs)
