import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENWEATHER_KEY: str = os.getenv("OPENWEATHER_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TRIPADVISOR_KEY: str = os.getenv("TRIPADVISOR_KEY", "")
    EXCHANGE_RATE_API_KEY: str = os.getenv("EXCHANGE_RATE_API_KEY", "")
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000"
    ).split(",")

    def validate(self):
        missing = [
            name
            for name in ("OPENWEATHER_KEY", "OPENAI_API_KEY", "TRIPADVISOR_KEY", "EXCHANGE_RATE_API_KEY")
            if not getattr(self, name)
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


settings = Settings()
