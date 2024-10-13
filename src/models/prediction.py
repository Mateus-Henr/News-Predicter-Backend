import enum

from pydantic import BaseModel


class PredictionEnum(enum.Enum):
    BUY = "BUY"
    NEUTRAL = "NEUTRAL"
    SELL = "SELL"


class AlertEnum(enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    MINIMAL = "MINIMAL"


class Prediction(BaseModel):
    prediction_value: PredictionEnum
    alert_level: AlertEnum
