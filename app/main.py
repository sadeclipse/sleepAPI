from contextlib import asynccontextmanager
import tensorflow as tf
from fastapi import FastAPI
from api.v1.routings import router
from database import Base, engine
from models.prediction import PredictionModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    app.state.ml_model = tf.keras.models.load_model("ml/model.keras")
    yield
    del app.state.ml_model


app = FastAPI(title="sleep API service", lifespan=lifespan)

app.include_router(router, prefix="/api/v1")
