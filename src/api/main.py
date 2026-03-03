import time
import uuid
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy.orm import Session

from src.api.schemas import PredictRequest, PredictResponse
from src.db.crud import create_prediction_log
from src.db.database import Base, engine, get_db

# --- Paths (same idea as train.py) ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "data" / "model" / "churn_model.joblib"

app = FastAPI(
    title="Churn Prediction API",
    version="1.0.0",
)

# -------------------------
# Prometheus metrics
# -------------------------
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
)

PREDICT_COUNT = Counter(
    "predict_requests_total",
    "Total number of /v1/predict calls",
)

PREDICT_ERRORS = Counter(
    "predict_errors_total",
    "Total number of prediction errors",
)


# --- Load model once when API starts ---
@app.on_event("startup")
def load_model():
    # Create DB tables if not exist
    Base.metadata.create_all(bind=engine)

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Train it first with: python -m src.ml.train"
        )
    app.state.model = joblib.load(MODEL_PATH)


# --- Middleware: request_id + Prometheus metrics ---
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = request_id

    endpoint = request.url.path
    start = time.time()

    status_code = 500  # default if something crashes before response exists
    try:
        response = await call_next(request)
        status_code = response.status_code

        # Add request id back in response headers (so client can reference it)
        response.headers["X-Request-Id"] = request_id
        response.headers["X-Response-Time-ms"] = str(int((time.time() - start) * 1000))
        return response
    finally:
        duration = time.time() - start
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(
            method=request.method, endpoint=endpoint, http_status=str(status_code)
        ).inc()


@app.get("/health")
def health():
    # Simple endpoint for Kubernetes / load balancers later
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/v1/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, request: Request, db: Session = Depends(get_db)):
    request_id = request.state.request_id
    start = time.time()

    # Count predict calls
    PREDICT_COUNT.inc()

    try:
        # Convert input to a single-row pandas DataFrame (model expects a table-like input)
        row: Dict[str, Any] = payload.model_dump()
        X = pd.DataFrame([row])

        model = app.state.model

        # Predict probability of churn (class 1)
        proba = float(model.predict_proba(X)[:, 1][0])
        label = int(proba >= 0.5)

        latency_ms = int((time.time() - start) * 1000)

        # Save to Postgres
        create_prediction_log(
            db=db,
            request_id=request_id,
            payload=row,
            churn_probability=proba,
            churn_label=label,
            latency_ms=latency_ms,
        )

        return PredictResponse(
            request_id=request_id,
            churn_probability=round(proba, 6),
            churn_label=label,
        )
    except Exception:
        # Count prediction errors (then re-raise so global handler returns 500 JSON)
        PREDICT_ERRORS.inc()
        raise


# Nice JSON error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "request_id": request_id},
    )