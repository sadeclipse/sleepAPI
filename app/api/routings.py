from fastapi.routing import APIRouter
from fastapi import status

from app.schemas import PredictionRequest, PredictionResponse

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def healt_check():
    return {"status": "OK"}


# add validation...
@router.post("/predict")
async def predict(health_data: PredictionRequest) -> PredictionResponse:
    return {""}
