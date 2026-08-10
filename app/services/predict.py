import io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import shap
import tensorflow as tf
from fastapi import Response, HTTPException
from schemas import HealthMetrics, PredictionResponse
from data_access_layer.pred_repo import PredictionRepository


class PredictService:
    def __init__(self, model: tf.keras.Model, repository: PredictionRepository):
        self.model = model
        self.repo = repository

    def predict_and_save(self, data: HealthMetrics) -> PredictionResponse:
        raw_dict = data.model_dump()

        transformed_dict = raw_dict.copy()
        transformed_dict["sleep_deviation"] = abs(
            8.0 - transformed_dict.pop("daily_sleep_hours")
        )
        transformed_dict["deep_sleep_hours"] = abs(
            1.75 - transformed_dict["deep_sleep_hours"]
        )

        cat_cols = ["gender", "physical_activity_level", "diet_type"]
        tf_inputs = {}
        for key, val in transformed_dict.items():
            if key in cat_cols:
                tf_inputs[key] = np.array([val], dtype=object)
            else:
                tf_inputs[key] = np.array([val], dtype=np.float32)

        class_pred, num_pred = self.model.predict(tf_inputs)

        predicted_score = round(
            max(
                0.1, min(9.9, float(num_pred if len(num_pred.shape) > 1 else num_pred))
            ),
            2,
        )
        stress_mapping = {0: "High", 1: "Low", 2: "Medium"}
        predicted_stress = stress_mapping.get(int(np.argmax(class_pred)), "Medium")

        db_record = self.repo.create(
            raw_features=raw_dict, score=predicted_score, stress_level=predicted_stress
        )

        return PredictionResponse(
            id=db_record.id,
            sleep_quality_score=predicted_score,
            daily_stress_level=predicted_stress,
        )

    def get_prediction_by_id(self, prediction_id: int) -> PredictionResponse:
        db_record = self.repo.get_by_id(prediction_id=prediction_id)
        if db_record is None:
            raise HTTPException(
                status_code=404, detail=f"Prediction with id {prediction_id} not found"
            )
        return PredictionResponse(
            id=db_record.id,
            sleep_quality_score=db_record.sleep_quality_score,
            daily_stress_level=db_record.daily_stress_level,
        )
