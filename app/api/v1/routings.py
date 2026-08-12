from fastapi import APIRouter, Depends, Request, Response
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
    explainer = getattr(request.app.state, "shap_explainer", None)
    return PredictService(model=model, repository=repository, explainer=explainer)


@router.post("/predict", response_model=PredictionResponse)
def predict_data(
    data: HealthMetrics, service: PredictService = Depends(get_predict_service)
):
    return service.predict_and_save(data=data)


@router.get("/predict/{id}")
def get_data(id: int, service: PredictService = Depends(get_predict_service)):
    return service.get_prediction_by_id(prediction_id=id)


@router.get(
    "/predict/{id}/explanation", responses={200: {"content": {"image/png": {}}}}
)
def get_shap_explanation(
    id: int, service: PredictService = Depends(get_predict_service)
):
    image_bytes = service.generate_shap_waterfall(prediction_id=id)
    return Response(content=image_bytes, media_type="image/png")
