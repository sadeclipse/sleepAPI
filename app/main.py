from contextlib import asynccontextmanager
import pandas as pd
import shap
import tensorflow as tf
from fastapi import FastAPI
from api.v1.routings import router
from database import Base, engine

MAPPINGS = {
    "gender": {"male": 0, "female": 1, "other": 2},
    "physical_activity_level": {"Low": 0, "Medium": 1, "High": 2},
    "diet_type": {"Unhealthy": 0, "Average": 1, "Healthy": 2},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    model = tf.keras.models.load_model("ml/model.keras")
    app.state.ml_model = model

    bg_df = pd.read_csv("ml/background.csv")
    bg_df = bg_df.drop(
        columns=["daily_stress_level", "sleep_quality_score"], errors="ignore"
    )

    bg_df_numeric = bg_df.copy()
    for col, mapping in MAPPINGS.items():
        if col in bg_df_numeric.columns:
            bg_df_numeric[col] = bg_df_numeric[col].map(mapping).fillna(0).astype(int)

    def model_predict_wrapper(x_dict):
        tf_inputs = {}
        for col in bg_df.columns:
            if col in MAPPINGS:
                tf_inputs[col] = (
                    x_dict[col].astype(int).astype(str).values.reshape(-1, 1)
                )
            else:
                tf_inputs[col] = x_dict[col].values.reshape(-1, 1)

        _, num_pred = model(tf_inputs, training=False)
        return num_pred.numpy().flatten()

    masker = shap.maskers.Independent(bg_df_numeric)
    app.state.shap_explainer = shap.Explainer(
        model_predict_wrapper, masker, feature_names=list(bg_df.columns)
    )

    yield
    del app.state.ml_model
    del app.state.shap_explainer


app = FastAPI(title="sleep API service", lifespan=lifespan)

app.include_router(router, prefix="/api/v1")
