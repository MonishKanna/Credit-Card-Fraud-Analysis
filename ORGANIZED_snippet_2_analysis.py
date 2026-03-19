"""
ORGANIZED SNIPPET 2: TRANSACTION ANALYSIS (UPDATED FOR SINGLE FILE)
===================================================================
Load transactions_data.csv (single file) and merge fraud labels
"""

import pandas as pd
import json

print("\n" + "=" * 80)
print("ORGANIZED SNIPPET 2: TRANSACTION ANALYSIS")
print("=" * 80)

# Load single transactions file
print("\n[STEP 1] Loading Transactions File...")
try:
    trans_df = pd.read_csv('transactions_data.csv')
    print(f"✓ Loaded: {len(trans_df):,} transactions")
    print(f"✓ Columns: {list(trans_df.columns)}")
except FileNotFoundError:
    print("✗ Error: transactions_data.csv not found in current folder")
    print("  Make sure you have transactions_data.csv in the fraud-detection folder")
    exit()

# Load fraud labels
print("\n[STEP 2] Loading Fraud Labels...")
try:
    with open('train_fraud_labels.json', 'r') as f:
        fraud_data = json.load(f)
    
    # Handle different JSON structures
    if 'root' in fraud_data and 'target' in fraud_data['root']:
        fraud_labels = fraud_data['root']['target']
    else:
        fraud_labels = fraud_data.get('target', fraud_data)
    
    fraud_df = pd.DataFrame(list(fraud_labels.items()), columns=['id', 'is_fraud'])
    fraud_df['id'] = fraud_df['id'].astype(int)
    print(f"✓ Fraud labels: {len(fraud_df):,}")
except FileNotFoundError:
    print("⚠️  Warning: train_fraud_labels.json not found")
    print("   Continuing without fraud labels...")
    fraud_df = None
except Exception as e:
    print(f"⚠️  Warning: Could not load fraud labels: {e}")
    fraud_df = None

# Merge with fraud labels
print("\n[STEP 3] Merging Transactions with Fraud Labels...")
if fraud_df is not None:
    trans_df = trans_df.merge(fraud_df, left_on='id', right_on='id', how='left')
    print(f"✓ Merged: {len(trans_df):,} rows")
    
    # Statistics
    print(f"\nFraud Distribution:")
    if 'is_fraud' in trans_df.columns:
        fraud_counts = trans_df['is_fraud'].value_counts(dropna=False)
        print(fraud_counts)
        
        labeled = trans_df['is_fraud'].notna().sum()
        total = len(trans_df)
        print(f"\nLabled transactions: {labeled:,} ({labeled/total*100:.1f}%)")
        
        if (trans_df['is_fraud'] == 'Yes').sum() > 0:
            fraud_count = (trans_df['is_fraud'] == 'Yes').sum()
            fraud_rate = fraud_count / labeled * 100
            print(f"Fraudulent: {fraud_count:,} ({fraud_rate:.2f}%)")
else:
    print("⚠️  No fraud labels - continuing without them")
    if 'is_fraud' not in trans_df.columns:
        trans_df['is_fraud'] = None

# Clean amount
print("\n[STEP 4] Cleaning Data...")

def clean_amount(val):
    """Convert amount to float, handling $ and commas"""
    if isinstance(val, str):
        try:
            return float(val.replace('$', '').replace(',', ''))
        except:
            return None
    try:
        return float(val)
    except:
        return None

# Check if 'amount' column exists
if 'amount' in trans_df.columns:
    trans_df['amount'] = trans_df['amount'].apply(clean_amount)
    print(f"✓ Amount column cleaned")

# Convert date if it exists
if 'date' in trans_df.columns:
    trans_df['date'] = pd.to_datetime(trans_df['date'], errors='coerce')
    print(f"✓ Date column converted")

# Handle missing values
print(f"\nMissing values before cleaning:")
missing_before = trans_df.isnull().sum()
if missing_before.sum() > 0:
    print(missing_before[missing_before > 0])
else:
    print("  None")

# Fill common missing values
numeric_cols = trans_df.select_dtypes(include=['number']).columns
for col in numeric_cols:
    if trans_df[col].isnull().sum() > 0:
        trans_df[col].fillna(trans_df[col].median(), inplace=True)

print(f"\n✓ Data cleaned: {len(trans_df):,} rows remaining")

# Show data info
print(f"\nData Info:")
print(f"  Shape: {trans_df.shape}")
print(f"  Memory: {trans_df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# Summary statistics
print(f"\nTransaction Summary:")
if 'amount' in trans_df.columns and trans_df['amount'].notna().sum() > 0:
    print(f"  Amount: ${trans_df['amount'].min():.2f} to ${trans_df['amount'].max():.2f}")
    print(f"  Average: ${trans_df['amount'].mean():.2f}")
    print(f"  Median: ${trans_df['amount'].median():.2f}")

if 'date' in trans_df.columns and trans_df['date'].notna().sum() > 0:
    print(f"  Date Range: {trans_df['date'].min()} to {trans_df['date'].max()}")

# Save combined dataset
print("\n[STEP 5] Saving Combined Data...")
trans_df.to_csv('transactions_combined.csv', index=False)
print("✓ Saved: transactions_combined.csv")

# Save summary stats
import json
summary = {
    'total_rows': len(trans_df),
    'total_columns': len(trans_df.columns),
    'columns': list(trans_df.columns),
    'memory_mb': float(trans_df.memory_usage(deep=True).sum() / 1024**2),
}

if 'is_fraud' in trans_df.columns:
    summary['fraud_stats'] = {
        'labeled': int(trans_df['is_fraud'].notna().sum()),
        'fraudulent': int((trans_df['is_fraud'] == 'Yes').sum()) if (trans_df['is_fraud'] == 'Yes').sum() > 0 else 0,
        'legitimate': int((trans_df['is_fraud'] != 'Yes').sum()) if (trans_df['is_fraud'] != 'Yes').sum() > 0 else 0,
    }

with open('summary_stats.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("✓ Saved: summary_stats.json")

print("\n" + "=" * 80)
print("✓ SNIPPET 2 COMPLETE")
print("=" * 80)
print("\nNext: python ORGANIZED_snippet_3_features.py")