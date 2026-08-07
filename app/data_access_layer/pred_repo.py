from sqlalchemy.orm import Session
from models.prediction import PredictionModel


class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, raw_features: dict, score: float, stress_level: str
    ) -> PredictionModel:
        db_prediction = PredictionModel(
            sleep_quality_score=score, daily_stress_level=stress_level, **raw_features
        )
        self.db.add(db_prediction)
        self.db.commit()
        self.db.refresh(db_prediction)
        return db_prediction

    def get_by_id(self, prediction_id: int) -> PredictionModel | None:
        return (
            self.db.query(PredictionModel)
            .filter(PredictionModel.id == prediction_id)
            .first()
        )
