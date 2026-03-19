"""
ORGANIZED SNIPPET 4: MODEL TRAINING
====================================
Train 3 ML models and evaluate
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import json
import warnings
warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("ORGANIZED SNIPPET 4: MODEL TRAINING")
print("=" * 80)

# Load data
print("\n[STEP 1] Loading Data...")
trans_df = pd.read_csv('transactions_engineered.csv')
with open('feature_columns.pkl', 'rb') as f:
    feature_cols = pickle.load(f)

print(f"✓ Loaded: {len(trans_df):,} rows, {len(feature_cols)} features")

# Prepare data
print("\n[STEP 2] Preparing Data...")
X = trans_df[feature_cols].copy()
y = trans_df['is_fraud_binary'].copy()

# Fill NaN
X = X.fillna(X.median())

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print(f"Train: {len(X_train):,}, Test: {len(X_test):,}")

# Scale
print("\n[STEP 3] Scaling Features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_scaled = np.nan_to_num(X_train_scaled, nan=0.0)
X_test_scaled = np.nan_to_num(X_test_scaled, nan=0.0)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✓ Scaler saved")

# Train models
print("\n[STEP 4] Training Models...")
models = {}

# Random Forest
print("  Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=15, class_weight='balanced', n_jobs=-1, random_state=42)
rf.fit(X_train_scaled, y_train)
models['random_forest'] = rf

# Gradient Boosting
print("  Training Gradient Boosting...")
gb = GradientBoostingClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
gb.fit(X_train_scaled, y_train)
models['gradient_boosting'] = gb

# Logistic Regression
print("  Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, class_weight='balanced', n_jobs=-1, random_state=42)
lr.fit(X_train_scaled, y_train)
models['logistic_regression'] = lr

print("✓ All models trained")

# Evaluate
print("\n[STEP 5] Evaluating Models...")
results = {}

for name, model in models.items():
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print(f"\n{name.upper()}:")
    print(f"  Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"  Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"  F1: {f1_score(y_test, y_pred):.4f}")
    
    try:
        auc = roc_auc_score(y_test, y_proba)
        print(f"  ROC-AUC: {auc:.4f}")
    except:
        print(f"  ROC-AUC: N/A")
    
    results[name] = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1': float(f1_score(y_test, y_pred))
    }

# Save models
print("\n[STEP 6] Saving Models...")
for name, model in models.items():
    with open(f'{name}_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Saved: {name}_model.pkl")

# Save evaluation
with open('model_evaluation.json', 'w') as f:
    json.dump(results, f, indent=2)
print("✓ Saved: model_evaluation.json")

print("\n" + "=" * 80)
print("✓ SNIPPET 4 COMPLETE")
print("=" * 80)
print("\nNext: python ORGANIZED_snippet_5_api.py")
