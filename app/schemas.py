from typing import Literal
from pydantic import BaseModel, Field, NonNegativeInt, NonNegativeFloat


class HealthMetrics(BaseModel):
    age: int = Field(..., gt=0, le=120, description="Возраст в годах")
    gender: Literal["male", "female", "other"] = Field(..., description="Пол")
    physical_activity_level: Literal["Medium", "Low", "High"] = Field(
        ..., description="Уровень физической активности"
    )
    diet_type: Literal["Average", "Healthy", "Unhealthy"] = Field(
        ..., description="Тип питания"
    )

    bmi: float = Field(..., gt=10.0, lt=60.0, description="Индекс массы тела")
    caffeine_intake_mg: NonNegativeInt = Field(
        ..., description="Потребление кофеина в мг"
    )
    water_intake_liters: NonNegativeFloat = Field(
        ..., description="Потребление воды в литрах"
    )
    screen_time_hours: float = Field(
        ..., ge=0.0, le=24.0, description="Экранное время в часах"
    )
    daily_steps: NonNegativeInt = Field(..., description="Количество шагов за день")
    calories_burned: NonNegativeInt = Field(..., description="Сожженные калории (ккал)")
    resting_heart_rate: int = Field(
        ..., ge=10, le=150, description="Пульс в покое (уд/мин)"
    )
    daily_sleep_hours: float = Field(
        ..., ge=0.0, le=24.0, description="Всего часов сна за сутки"
    )
    deep_sleep_hours: float = Field(
        ..., ge=0.0, le=24.0, description="Часов глубокого сна"
    )


class PredictionResponse(BaseModel):
    sleep_quality_score: float = Field(
        ..., gt=0.0, lt=10.0, description="Оценка качества сна"
    )
    daily_stress_level: Literal["Low", "Medium", "High"] = Field(
        ..., description="Уровень стресса в течение дна"
    )
