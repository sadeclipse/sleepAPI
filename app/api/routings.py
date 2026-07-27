from fastapi.routing import APIRouter
from fastapi import status

from app.schemas import PredictionRequest, PredictionResponse

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def healt_check():
    return {"status": "OK"}


@router.post("/predict")
async def predict(wine: PredictionRequest) -> PredictionResponse:
    return {"quality of wine": "to test it we will set it to 5"}
