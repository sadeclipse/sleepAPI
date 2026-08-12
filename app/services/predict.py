import io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import shap
import tensorflow as tf
from fastapi import Response, HTTPException
from schemas import HealthMetrics, PredictionResponse
from data_access_layer.pred_repo import PredictionRepository

MAPPINGS = {
    "gender": {"male": 0, "female": 1, "other": 2},
    "physical_activity_level": {"Low": 0, "Medium": 1, "High": 2},
    "diet_type": {"Unhealthy": 0, "Average": 1, "Healthy": 2},
}


class PredictService:
    def __init__(
        self,
        model: tf.keras.Model,
        repository: PredictionRepository,
        explainer: shap.Explainer = None,
    ):
        self.model = model
        self.repo = repository
        self.explainer = explainer

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

    def generate_shap_waterfall(self, prediction_id: int) -> bytes:
        db_record = self.repo.get_by_id(prediction_id=prediction_id)
        if db_record is None:
            raise HTTPException(status_code=404, detail="Prediction not found")

        raw_features = {
            col.name: getattr(db_record, col.name)
            for col in db_record.__table__.columns
            if col.name
            not in ["id", "created_at", "sleep_quality_score", "daily_stress_level"]
        }

        transformed_features = raw_features.copy()
        transformed_features["sleep_deviation"] = abs(
            8.0 - transformed_features["daily_sleep_hours"]
        )
        transformed_features["deep_sleep_hours"] = abs(
            1.75 - transformed_features["deep_sleep_hours"]
        )

        if "daily_sleep_hours" in transformed_features:
            del transformed_features["daily_sleep_hours"]

        for col, mapping in MAPPINGS.items():
            if col in transformed_features:
                val = transformed_features[col]
                transformed_features[col] = mapping.get(val, 0)

        for k in transformed_features:
            if k not in MAPPINGS:
                transformed_features[k] = float(transformed_features[k])

        feature_order = self.explainer.feature_names
        instance_df = pd.DataFrame([transformed_features])[feature_order]

        shap_values = self.explainer(instance_df)

        plt.figure(figsize=(10, 6))
        shap.plots.waterfall(shap_values[0], show=False)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)
        plt.close()
        buf.seek(0)

        return buf.getvalue()
