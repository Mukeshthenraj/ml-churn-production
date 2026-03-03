from typing import Optional, Literal
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    # Keep fields optional so your API doesn't crash if a field is missing.
    # Missing values will be handled by the same preprocessing pipeline you trained with.

    gender: Optional[str] = None
    SeniorCitizen: Optional[int] = Field(default=None, description="0 or 1")
    Partner: Optional[str] = None
    Dependents: Optional[str] = None
    tenure: Optional[float] = None
    PhoneService: Optional[str] = None
    MultipleLines: Optional[str] = None
    InternetService: Optional[str] = None
    OnlineSecurity: Optional[str] = None
    OnlineBackup: Optional[str] = None
    DeviceProtection: Optional[str] = None
    TechSupport: Optional[str] = None
    StreamingTV: Optional[str] = None
    StreamingMovies: Optional[str] = None
    Contract: Optional[str] = None
    PaperlessBilling: Optional[str] = None
    PaymentMethod: Optional[str] = None
    MonthlyCharges: Optional[float] = None
    TotalCharges: Optional[float] = None


class PredictResponse(BaseModel):
    request_id: str
    churn_probability: float
    churn_label: Literal[0, 1]
