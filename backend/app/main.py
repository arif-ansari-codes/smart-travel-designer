from app.core.logging_config import configure_logging

configure_logging()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import weather, tripadvisor, exchange, tripplan

app = FastAPI(title="AI Trip Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(weather.router, prefix="/weather")
app.include_router(tripadvisor.router)
app.include_router(exchange.router)
app.include_router(tripplan.router)


@app.get("/")
def welcome():
    return {"message": "Welcome to the AI Trip Planner API"}
