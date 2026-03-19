"""
ORGANIZED SNIPPET 1: EXPLORATORY DATA ANALYSIS
===============================================
Load and analyze user, card, and merchant data
"""

import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print("ORGANIZED SNIPPET 1: EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# Load users
users_df = pd.read_csv('users_data.csv')
print(f"✓ Users: {len(users_df):,}")

# Load cards
cards_df = pd.read_csv('cards_data.csv')
print(f"✓ Cards: {len(cards_df):,}")

# Load MCC codes
with open('mcc_codes.json', 'r') as f:
    mcc_codes = json.load(f)
print(f"✓ MCC Codes: {len(mcc_codes)}")

# Clean currency
def clean_currency(val):
    if isinstance(val, str):
        return float(val.replace('$', '').replace(',', ''))
    return float(val)

users_df['per_capita_income'] = users_df['per_capita_income'].apply(clean_currency)
users_df['yearly_income'] = users_df['yearly_income'].apply(clean_currency)
users_df['total_debt'] = users_df['total_debt'].apply(clean_currency)
cards_df['credit_limit'] = cards_df['credit_limit'].apply(clean_currency)

# Statistics
print(f"\nUsers Age: {users_df['current_age'].min()}-{users_df['current_age'].max()}")
print(f"Credit Score: {users_df['credit_score'].min()}-{users_df['credit_score'].max()}")
print(f"Card Types: {cards_df['card_type'].value_counts().to_dict()}")

# Save
users_df.to_csv('users_df.csv', index=False)
cards_df.to_csv('cards_df.csv', index=False)
mcc_df = pd.DataFrame(list(mcc_codes.items()), columns=['mcc_code', 'merchant_category'])
mcc_df.to_csv('mcc_df.csv', index=False)

print("\n✓ SNIPPET 1 COMPLETE\nNext: python ORGANIZED_snippet_2_analysis.py")
