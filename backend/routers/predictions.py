import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.models.models import Prediction, User
from backend.schemas.schemas import PredictionRequest, PredictionResponse
from ml.predictor import predictor_instance
from ml.train import train_delay_model
from backend.core.security import get_current_user, require_role

router = APIRouter(prefix="/api/v1/predictions", tags=["ML Delay Predictions"])

@router.post("/predict", response_model=PredictionResponse)
def predict_flight_delay(req: PredictionRequest, db: Session = Depends(get_db)):
    features = req.model_dump()
    res = predictor_instance.predict(features)

    # Persist prediction in DB warehouse
    pred_obj = Prediction(
        flight_identifier=req.flight_identifier,
        origin_iata=req.origin_iata,
        destination_iata=req.destination_iata,
        delay_probability=res["delay_probability"],
        expected_delay_mins=res["expected_delay_mins"],
        confidence_score=res["confidence_score"],
        risk_level=res["risk_level"],
        feature_snapshot=features
    )
    db.add(pred_obj)
    db.commit()

    return {
        "flight_identifier": req.flight_identifier,
        "origin_iata": req.origin_iata,
        "destination_iata": req.destination_iata,
        "delay_probability": res["delay_probability"],
        "delay_probability_pct": res["delay_probability_pct"],
        "expected_delay_mins": res["expected_delay_mins"],
        "confidence_score": res["confidence_score"],
        "risk_level": res["risk_level"],
        "feature_importances": res["feature_importances"],
        "shap_contributions": res["shap_contributions"]
    }

@router.post("/retrain")
def retrain_model(current_user: User = Depends(require_role(["admin", "analyst"]))):
    try:
        artifact = train_delay_model()
        predictor_instance.load_model()
        return {
            "status": "SUCCESS",
            "message": "Delay prediction model successfully retrained and reloaded into active memory.",
            "metrics": artifact["metrics"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrain model: {str(e)}")

@router.get("/history")
def get_prediction_history(limit: int = 50, db: Session = Depends(get_db)):
    preds = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(limit).all()
    return preds
