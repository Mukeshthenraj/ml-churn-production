import json
from sqlalchemy.orm import Session

from src.db.models import PredictionLog


def create_prediction_log(
    db: Session,
    request_id: str,
    payload: dict,
    churn_probability: float,
    churn_label: int,
    latency_ms: int,
) -> PredictionLog:
    row = PredictionLog(
        request_id=request_id,
        input_json=json.dumps(payload, ensure_ascii=False),
        churn_probability=churn_probability,
        churn_label=churn_label,
        latency_ms=latency_ms,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row