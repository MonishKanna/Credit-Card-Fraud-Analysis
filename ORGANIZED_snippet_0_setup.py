"""
===============================================================================
FRAUD DETECTION SYSTEM - ORGANIZED PROJECT STRUCTURE
===============================================================================
A comprehensive, production-ready fraud detection pipeline

Project Structure:
  snippet_0_setup.py                    - Setup & Dependencies
  snippet_1_eda.py                      - Exploratory Data Analysis
  snippet_2_transaction_analysis.py     - Transaction Data Analysis
  snippet_3_feature_engineering.py      - Feature Engineering
  snippet_4_model_training.py           - Model Training & Evaluation
  snippet_5_fastapi_deployment.py       - API Deployment
  test_api.py                           - API Testing
  requirements.txt                      - Python Dependencies

===============================================================================
SNIPPET 0: SETUP & CONFIGURATION
===============================================================================
"""

import sys
import warnings
warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("FRAUD DETECTION SYSTEM - SETUP & CONFIGURATION")
print("=" * 80)

# ============= STEP 1: INSTALL DEPENDENCIES =============
print("\n[STEP 1] Installing Dependencies...")

import subprocess

dependencies = [
    'pandas',
    'numpy',
    'scikit-learn',
    'fastapi',
    'uvicorn',
    'pydantic',
    'python-multipart'
]

print("Required packages:")
for pkg in dependencies:
    print(f"  • {pkg}")

# ============= STEP 2: IMPORT LIBRARIES =============
print("\n[STEP 2] Importing Libraries...")

import pandas as pd
import numpy as np
import json
import pickle
import os
from datetime import datetime
from typing import Dict, List
import logging

print("✓ Core libraries imported")

# ============= STEP 3: SETUP LOGGING =============
print("\n[STEP 3] Setting Up Logging...")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Logging configured")

# ============= STEP 4: DEFINE GLOBAL PATHS =============
print("\n[STEP 4] Defining Data Paths...")

DATA_PATHS = {
    'users': 'users_data.csv',
    'cards': 'cards_data.csv',
    'mcc_codes': 'mcc_codes.json',
    'transactions_pattern': 'transactions_part*.csv',
    'fraud_labels': 'train_fraud_labels.json',
}

OUTPUT_PATHS = {
    'processed_users': 'users_df.csv',
    'processed_cards': 'cards_df.csv',
    'mcc_lookup': 'mcc_df.csv',
    'combined_transactions': 'transactions_combined.csv',
    'engineered_features': 'transactions_engineered.csv',
    'scaler': 'scaler.pkl',
    'feature_columns': 'feature_columns.pkl',
    'models': {
        'random_forest': 'random_forest_model.pkl',
        'gradient_boosting': 'gradient_boosting_model.pkl',
        'logistic_regression': 'logistic_regression_model.pkl',
    },
    'metadata': {
        'features': 'feature_metadata.json',
        'evaluation': 'model_evaluation.json',
        'summary': 'summary_stats.json',
    }
}

print("Data paths configured:")
for key, value in DATA_PATHS.items():
    print(f"  {key}: {value}")

# ============= STEP 5: HELPER FUNCTIONS =============
print("\n[STEP 5] Defining Helper Functions...")

def clean_currency(val):
    """Convert currency string (with $ signs) to float"""
    if isinstance(val, str):
        return float(val.replace('$', '').replace(',', ''))
    return float(val)

def load_data(filepath: str, data_type: str = 'csv') -> object:
    """Load data from CSV or JSON file"""
    try:
        if data_type == 'csv':
            return pd.read_csv(filepath)
        elif data_type == 'json':
            with open(filepath, 'r') as f:
                return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {filepath}")
        return None

def save_data(data: object, filepath: str, data_type: str = 'csv'):
    """Save data to CSV or pickle"""
    try:
        if data_type == 'csv':
            data.to_csv(filepath, index=False)
        elif data_type == 'pickle':
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
        logger.info(f"✓ Saved: {filepath}")
    except Exception as e:
        logger.error(f"Error saving {filepath}: {str(e)}")

print("✓ Helper functions defined")

# ============= STEP 6: ENVIRONMENT CHECK =============
print("\n[STEP 6] Checking Environment...")

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Available files: {len(os.listdir('.'))}")

# ============= STEP 7: COMPLETION =============
print("\n" + "=" * 80)
print("✓ SETUP COMPLETE - System ready for analysis")
print("=" * 80)

print("""
Next Steps:
  1. Run: python snippet_1_eda.py
  2. Run: python snippet_2_transaction_analysis.py
  3. Run: python snippet_3_feature_engineering.py
  4. Run: python snippet_4_model_training.py
  5. Run: python snippet_5_fastapi_deployment.py

Or import this file and use the helper functions:
  from snippet_0_setup import load_data, save_data, DATA_PATHS, OUTPUT_PATHS
""")
