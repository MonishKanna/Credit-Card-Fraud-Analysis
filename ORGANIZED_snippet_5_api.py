"""
ORGANIZED SNIPPET 5: FASTAPI DEPLOYMENT
========================================
Build REST API for fraud predictions
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
import numpy as np
import pandas as pd
import pickle
import json
import os

print("Loading models...")

# Load models
models = {}
for model_name in ['random_forest', 'gradient_boosting', 'logistic_regression']:
    try:
        with open(f'{model_name}_model.pkl', 'rb') as f:
            models[model_name] = pickle.load(f)
    except:
        pass

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

with open('feature_metadata.json', 'r') as f:
    metadata = json.load(f)

print(f"✓ Loaded {len(models)} models")

# Create app
app = FastAPI(title="Fraud Detection API", version="1.0.0")

# Request model
class TransactionRequest(BaseModel):
    amount: float
    transaction_hour: int
    transaction_day: int
    transaction_month: int
    transaction_dayofweek: int
    transaction_dayofyear: int
    use_chip: str
    card_amount_mean: float
    card_amount_std: float
    card_amount_min: float
    card_amount_max: float
    card_txn_count: int
    card_unique_days: int
    merchant_fraud_rate: float
    merchant_txn_count: int
    state_fraud_rate: float
    state_txn_count: int
    current_age: int
    credit_score: int
    yearly_income: float
    customer_fraud_rate: float
    amount_z_score: float
    amount_vs_customer_avg: float
    model: str = "ensemble"

class PredictionResponse(BaseModel):
    fraud_prediction: bool
    fraud_probability: float
    confidence_score: float
    risk_level: str
    model_used: str
    explanation: Dict

# Endpoints
@app.get("/")
def root():
    return {"message": "Fraud Detection API", "docs_url": "/docs"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "models_loaded": list(models.keys()),
        "features_count": len(feature_columns)
    }

@app.get("/models")
def list_models():
    return {"available_models": list(models.keys())}

def get_risk_level(prob):
    if prob < 0.3:
        return "LOW"
    elif prob < 0.6:
        return "MEDIUM"
    elif prob < 0.8:
        return "HIGH"
    else:
        return "CRITICAL"

@app.post("/predict", response_model=PredictionResponse)
def predict_fraud(transaction: TransactionRequest):
    # Create features dict
    features_dict = {
        'amount': transaction.amount,
        'transaction_hour': transaction.transaction_hour,
        'transaction_day': transaction.transaction_day,
        'transaction_month': transaction.transaction_month,
        'transaction_dayofweek': transaction.transaction_dayofweek,
        'transaction_dayofyear': transaction.transaction_dayofyear,
        'amount_log': np.log1p(abs(transaction.amount)),
        'amount_is_negative': 0,
        'is_online': 1 if 'Online' in transaction.use_chip else 0,
        'is_swipe': 1 if 'Swipe' in transaction.use_chip else 0,
        'card_amount_mean': transaction.card_amount_mean,
        'card_amount_std': transaction.card_amount_std,
        'card_amount_min': transaction.card_amount_min,
        'card_amount_max': transaction.card_amount_max,
        'card_txn_count': transaction.card_txn_count,
        'card_unique_days': transaction.card_unique_days,
        'merchant_fraud_rate': transaction.merchant_fraud_rate,
        'merchant_txn_count': transaction.merchant_txn_count,
        'state_fraud_rate': transaction.state_fraud_rate,
        'state_txn_count': transaction.state_txn_count,
        'current_age': transaction.current_age,
        'credit_score': transaction.credit_score,
        'yearly_income': transaction.yearly_income,
        'customer_fraud_rate': transaction.customer_fraud_rate,
        'amount_z_score': transaction.amount_z_score,
        'amount_vs_customer_avg': transaction.amount_vs_customer_avg,
    }
    
    features_df = pd.DataFrame([features_dict])
    for col in feature_columns:
        if col not in features_df.columns:
            features_df[col] = 0
    
    features_df = features_df[feature_columns]
    features_scaled = scaler.transform(features_df)
    features_scaled = np.nan_to_num(features_scaled, nan=0.0)
    
    # Predict
    if transaction.model == "ensemble":
        probs = [model.predict_proba(features_scaled)[0, 1] for model in models.values()]
        fraud_prob = float(np.mean(probs))
        model_used = "ensemble"
    else:
        if transaction.model not in models:
            fraud_prob = 0.5
            model_used = "default"
        else:
            fraud_prob = float(models[transaction.model].predict_proba(features_scaled)[0, 1])
            model_used = transaction.model
    
    is_fraud = fraud_prob > 0.5
    confidence = max(fraud_prob, 1 - fraud_prob)
    
    return PredictionResponse(
        fraud_prediction=is_fraud,
        fraud_probability=round(fraud_prob, 4),
        confidence_score=round(confidence, 4),
        risk_level=get_risk_level(fraud_prob),
        model_used=model_used,
        explanation={
            "amount": f"${transaction.amount:.2f}",
            "recommendation": "BLOCK" if is_fraud else "APPROVE"
        }
    )

if __name__ == "__main__":
    import uvicorn
    print("\nStarting API on http://localhost:8000")
    print("Swagger UI: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
