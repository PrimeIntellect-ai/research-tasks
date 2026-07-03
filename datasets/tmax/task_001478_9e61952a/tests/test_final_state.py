# test_final_state.py
import os
import pytest
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def test_model_input_parquet_exists():
    assert os.path.isfile('/home/user/model_input.parquet'), "The file /home/user/model_input.parquet does not exist."

def test_model_input_columns():
    df = pd.read_parquet('/home/user/model_input.parquet')
    expected_columns = ['pca_1', 'pca_2', 'churn']
    assert list(df.columns) == expected_columns, f"Columns in parquet file do not match exactly. Expected {expected_columns}, got {list(df.columns)}."

def test_logistic_regression_accuracy():
    df = pd.read_parquet('/home/user/model_input.parquet')
    X = df[['pca_1', 'pca_2']]
    y = df['churn']

    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    preds = model.predict(X)
    acc = accuracy_score(y, preds)

    assert acc >= 0.80, f"Logistic Regression accuracy is {acc}, which is below the required threshold of 0.80."