"""
ORGANIZED SNIPPET 3: FEATURE ENGINEERING
=========================================
Create 26 features for machine learning
"""

import pandas as pd
import numpy as np
import json

print("\n" + "=" * 80)
print("ORGANIZED SNIPPET 3: FEATURE ENGINEERING")
print("=" * 80)

# Load data
print("\n[STEP 1] Loading Data...")
trans_df = pd.read_csv('transactions_combined.csv')
users_df = pd.read_csv('users_df.csv')
cards_df = pd.read_csv('cards_df.csv')
print(f"✓ Loaded: {len(trans_df):,} transactions")

# Clean
trans_df['date'] = pd.to_datetime(trans_df['date'])

# Temporal features
print("\n[STEP 2] Creating Temporal Features...")
trans_df['transaction_hour'] = trans_df['date'].dt.hour
trans_df['transaction_day'] = trans_df['date'].dt.day
trans_df['transaction_month'] = trans_df['date'].dt.month
trans_df['transaction_dayofweek'] = trans_df['date'].dt.dayofweek
trans_df['transaction_dayofyear'] = trans_df['date'].dt.dayofyear

# Amount features
print("[STEP 3] Creating Amount Features...")
trans_df['amount_log'] = np.log1p(abs(trans_df['amount']))
trans_df['amount_is_negative'] = (trans_df['amount'] < 0).astype(int)

# Card features
print("[STEP 4] Creating Card Velocity Features...")
card_stats = trans_df.groupby('card_id').agg({
    'amount': ['mean', 'std', 'min', 'max', 'count'],
    'date': 'nunique'
})
card_stats.columns = ['card_amount_mean', 'card_amount_std', 'card_amount_min', 
                      'card_amount_max', 'card_txn_count', 'card_unique_days']
trans_df = trans_df.merge(card_stats, left_on='card_id', right_index=True, how='left')

# Merchant features
print("[STEP 5] Creating Merchant Features...")
merchant_fraud_rate = trans_df.groupby('merchant_id')['is_fraud'].apply(
    lambda x: (x == 'Yes').sum() / len(x) if len(x) > 0 else 0
).reset_index(name='merchant_fraud_rate')
trans_df = trans_df.merge(merchant_fraud_rate, on='merchant_id', how='left')

merchant_count = trans_df.groupby('merchant_id').size().reset_index(name='merchant_txn_count')
trans_df = trans_df.merge(merchant_count, on='merchant_id', how='left')

# Geographic features
print("[STEP 6] Creating Geographic Features...")
state_fraud = trans_df.dropna(subset=['merchant_state']).groupby('merchant_state')['is_fraud'].apply(
    lambda x: (x == 'Yes').sum() / len(x) if len(x) > 0 else 0
).reset_index(name='state_fraud_rate')
state_count = trans_df.groupby('merchant_state').size().reset_index(name='state_txn_count')
trans_df = trans_df.merge(state_fraud, on='merchant_state', how='left')
trans_df = trans_df.merge(state_count, on='merchant_state', how='left')

# Customer features
print("[STEP 7] Creating Customer Features...")
trans_df = trans_df.merge(users_df[['id', 'current_age', 'credit_score', 'yearly_income']], 
                          left_on='client_id', right_on='id', how='left')

customer_fraud_rate = trans_df.groupby('client_id')['is_fraud'].apply(
    lambda x: (x == 'Yes').sum() / len(x) if len(x) > 0 else 0
).reset_index(name='customer_fraud_rate')
trans_df = trans_df.merge(customer_fraud_rate, on='client_id', how='left')

# Amount deviation
print("[STEP 8] Creating Deviation Features...")
def calc_deviation(group):
    mean = group['amount'].mean()
    std = group['amount'].std()
    group['amount_z_score'] = (group['amount'] - mean) / (std + 0.0001)
    group['amount_vs_customer_avg'] = group['amount'] / (mean + 0.01)
    return group

trans_df = trans_df.groupby('client_id', group_keys=False).apply(calc_deviation)

# Transaction type
print("[STEP 9] Creating Transaction Type Features...")
trans_df['is_online'] = (trans_df['use_chip'] == 'Online Transaction').astype(int)
trans_df['is_swipe'] = (trans_df['use_chip'] == 'Swipe Transaction').astype(int)

# Handle missing
print("\n[STEP 10] Handling Missing Values...")
numeric_cols = trans_df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if trans_df[col].isnull().sum() > 0:
        trans_df[col].fillna(trans_df[col].median(), inplace=True)

# Feature list
feature_cols = ['amount', 'transaction_hour', 'transaction_day', 'transaction_month',
                'transaction_dayofweek', 'transaction_dayofyear', 'amount_log',
                'amount_is_negative', 'is_online', 'is_swipe', 'card_amount_mean',
                'card_amount_std', 'card_amount_min', 'card_amount_max',
                'card_txn_count', 'card_unique_days', 'merchant_fraud_rate',
                'merchant_txn_count', 'state_fraud_rate', 'state_txn_count',
                'current_age', 'credit_score', 'yearly_income', 'customer_fraud_rate',
                'amount_z_score', 'amount_vs_customer_avg']

# Convert fraud to binary
trans_df['is_fraud_binary'] = (trans_df['is_fraud'] == 'Yes').astype(int)

print(f"\n✓ Features created: {len(feature_cols)}")

# Save
print("\n[STEP 11] Saving...")
trans_df.to_csv('transactions_engineered.csv', index=False)

metadata = {
    'total_features': len(feature_cols),
    'features': feature_cols,
    'target': 'is_fraud_binary'
}
with open('feature_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

import pickle
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)

print("✓ Saved: transactions_engineered.csv")
print("✓ Saved: feature_metadata.json")
print("✓ Saved: feature_columns.pkl")

print("\n" + "=" * 80)
print("✓ SNIPPET 3 COMPLETE")
print("=" * 80)
print("\nNext: python ORGANIZED_snippet_4_training.py")
