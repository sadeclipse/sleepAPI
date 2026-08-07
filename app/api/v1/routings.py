from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from schemas import HealthMetrics, PredictionResponse
from data_access_layer.pred_repo import PredictionRepository
from services.predict import PredictService
from database import get_db

router = APIRouter(tags=["Sleep & Stress Predictions"])


def get_predict_service(
    request: Request, db: Session = Depends(get_db)
) -> PredictService:
    model = request.app.state.ml_model
    repository = PredictionRepository(db=db)
    return PredictService(model=model, repository=repository)


@router.post("/predict", response_model=PredictionResponse)
async def predict_data(
    payload: HealthMetrics, service: PredictService = Depends(get_predict_service)
):
    return service.predict_and_save(payload)
