"""
ORGANIZED TEST SUITE
====================
Comprehensive API testing
"""

import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000"

print("\n" + "=" * 80)
print("FRAUD DETECTION API - TEST SUITE")
print("=" * 80)

# Test 1: Health Check
print("\n[TEST 1] Health Check...")
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Status: {data['status']}")
        print(f"✓ Models: {data['models_loaded']}")
        print(f"✓ Features: {data['features_count']}")
    else:
        print(f"✗ Error: {resp.status_code}")
except Exception as e:
    print(f"✗ Error: {str(e)}")

# Test 2: Legitimate Transaction
print("\n[TEST 2] Legitimate Transaction...")
legit = {
    "amount": 50.00,
    "transaction_hour": 10,
    "transaction_day": 15,
    "transaction_month": 6,
    "transaction_dayofweek": 2,
    "transaction_dayofyear": 167,
    "use_chip": "Swipe Transaction",
    "card_amount_mean": 50.0,
    "card_amount_std": 25.0,
    "card_amount_min": 10.0,
    "card_amount_max": 150.0,
    "card_txn_count": 50,
    "card_unique_days": 20,
    "merchant_fraud_rate": 0.01,
    "merchant_txn_count": 1000,
    "state_fraud_rate": 0.02,
    "state_txn_count": 50000,
    "current_age": 35,
    "credit_score": 750,
    "yearly_income": 75000,
    "customer_fraud_rate": 0.0,
    "amount_z_score": 0.2,
    "amount_vs_customer_avg": 0.9,
    "model": "ensemble"
}

try:
    resp = requests.post(f"{BASE_URL}/predict", json=legit, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Fraud: {data['fraud_prediction']}")
        print(f"✓ Risk Level: {data['risk_level']}")
        print(f"✓ Probability: {data['fraud_probability']:.2%}")
    else:
        print(f"✗ Error: {resp.status_code}")
except Exception as e:
    print(f"✗ Error: {str(e)}")

# Test 3: Fraudulent Transaction
print("\n[TEST 3] Fraudulent Transaction...")
fraud = {
    "amount": 3000.00,
    "transaction_hour": 3,
    "transaction_day": 15,
    "transaction_month": 6,
    "transaction_dayofweek": 5,
    "transaction_dayofyear": 167,
    "use_chip": "Online Transaction",
    "card_amount_mean": 50.0,
    "card_amount_std": 25.0,
    "card_amount_min": 10.0,
    "card_amount_max": 150.0,
    "card_txn_count": 50,
    "card_unique_days": 20,
    "merchant_fraud_rate": 0.20,
    "merchant_txn_count": 100,
    "state_fraud_rate": 0.15,
    "state_txn_count": 5000,
    "current_age": 35,
    "credit_score": 550,
    "yearly_income": 35000,
    "customer_fraud_rate": 0.10,
    "amount_z_score": 5.0,
    "amount_vs_customer_avg": 60.0,
    "model": "ensemble"
}

try:
    resp = requests.post(f"{BASE_URL}/predict", json=fraud, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Fraud: {data['fraud_prediction']}")
        print(f"✓ Risk Level: {data['risk_level']}")
        print(f"✓ Probability: {data['fraud_probability']:.2%}")
    else:
        print(f"✗ Error: {resp.status_code}")
except Exception as e:
    print(f"✗ Error: {str(e)}")

# Test 4: Models
print("\n[TEST 4] List Models...")
try:
    resp = requests.get(f"{BASE_URL}/models", timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✓ Available models: {data['available_models']}")
    else:
        print(f"✗ Error: {resp.status_code}")
except Exception as e:
    print(f"✗ Error: {str(e)}")

print("\n" + "=" * 80)
print("✓ TEST SUITE COMPLETE")
print("=" * 80)
