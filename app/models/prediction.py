from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class PredictionModel(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Результаты вычислений сети
    sleep_quality_score = Column(Float, nullable=False)
    daily_stress_level = Column(String, nullable=False)

    # 13 Сырых входящих признаков от пользователя
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    physical_activity_level = Column(String, nullable=False)
    diet_type = Column(String, nullable=False)
    bmi = Column(Float, nullable=False)
    caffeine_intake_mg = Column(Integer, nullable=False)
    water_intake_liters = Column(Float, nullable=False)
    screen_time_hours = Column(Float, nullable=False)
    daily_steps = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    resting_heart_rate = Column(Integer, nullable=False)
    daily_sleep_hours = Column(Float, nullable=False)
    deep_sleep_hours = Column(Float, nullable=False)
