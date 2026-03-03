from sqlalchemy import Column, DateTime, Float, Integer, String, Text, func

from src.db.database import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(64), index=True, nullable=False)

    # Store input payload as JSON text (simple for now)
    input_json = Column(Text, nullable=False)

    churn_probability = Column(Float, nullable=False)
    churn_label = Column(Integer, nullable=False)

    latency_ms = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)