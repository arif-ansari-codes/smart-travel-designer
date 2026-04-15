from fastapi import APIRouter
from pydantic import BaseModel
from app.services.tripadvisor import get_tripadvisor_data

router = APIRouter()

class TripAdvisorRequest(BaseModel):
    city: str

@router.post("/tripadvisor/data")
def tripadvisor_data(req: TripAdvisorRequest):
    return get_tripadvisor_data(req.city)
