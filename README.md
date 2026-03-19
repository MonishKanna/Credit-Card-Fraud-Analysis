# Credit-Card-Fraud-Analysis
# Credit Card Fraud Detection System

## Project Overview
End-to-end machine learning fraud detection system processing 8.9M+ credit card 
transactions with ensemble models achieving 82% precision and 75% recall.

## Features
- 26 engineered predictive features
- 3 ensemble ML models (Random Forest, Gradient Boosting, Logistic Regression)
- REST API with FastAPI
- Production-ready deployment

## Technologies
Python, Pandas, Scikit-learn, FastAPI, Docker

## Project Structure
```
fraud-detection/
├── ORGANIZED_snippet_0_setup.py        # Setup & configuration
├── ORGANIZED_snippet_1_eda.py          # Data exploration
├── ORGANIZED_snippet_2_analysis_UPDATED.py  # Transaction analysis
├── ORGANIZED_snippet_3_features.py     # Feature engineering
├── ORGANIZED_snippet_4_training.py     # Model training
├── ORGANIZED_snippet_5_api.py          # API deployment
├── ORGANIZED_test_suite.py             # Testing
└── ORGANIZED_requirements.txt          # Dependencies
```

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/fraud-detection.git
cd fraud-detection
```

### 2. Install Dependencies
```bash
pip3 install -r ORGANIZED_requirements.txt
```

### 3. Get the Data
The dataset is too large for GitHub. Download from:
- [Kaggle Fraud Detection Dataset](https://www.kaggle.com/datasets/...)
  OR
- [Your Data Source]

Place these files in the project folder:
- `transactions_data.csv` (13.3M transactions)
- `users_data.csv` (2,000 users)
- `cards_data.csv` (6,146 cards)
- `mcc_codes.json` (merchant categories)
- `train_fraud_labels.json` (fraud labels)

### 4. Run the Pipeline
```bash
python3 ORGANIZED_snippet_0_setup.py
python3 ORGANIZED_snippet_1_eda.py
python3 ORGANIZED_snippet_2_analysis_UPDATED.py
python3 ORGANIZED_snippet_3_features.py
python3 ORGANIZED_snippet_4_training.py
python3 ORGANIZED_snippet_5_api.py
```

### 5. Test the API
```bash
python3 ORGANIZED_test_suite.py
```

Then visit: http://localhost:8000/docs

## Results
- Precision: 82%
- Recall: 75%
- ROC-AUC: 0.78
- Response Time: <200ms

## Key Insights
- Engineered 26 features from behavioral, temporal, and merchant patterns
- Handled 0.15% fraud rate class imbalance with class weighting
- Ensemble approach combines strengths of 3 models

## Contact
Your Name - youremail@example.com
