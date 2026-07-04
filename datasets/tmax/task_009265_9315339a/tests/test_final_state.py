# test_final_state.py

import os
import csv
import subprocess
import pytest

PREDICTIONS_FILE = "/home/user/predictions.csv"
METRICS_FILE = "/home/user/metrics.txt"
RAW_DATA_FILE = "/home/user/data/raw_data.csv"

def get_expected_mse():
    """
    Computes the expected MSE by running a subprocess that uses pandas and sklearn.
    This avoids importing third-party libraries directly in the pytest file.
    """
    script = """
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

df = pd.read_csv('/home/user/data/raw_data.csv')
df['date'] = pd.to_datetime(df['date'], mixed_dayfirst=False)
df['month'] = df['date'].dt.month
df['price'] = df['price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
df['zip_code'] = df['zip_code'].astype(str)

dummies = pd.get_dummies(df['zip_code'], prefix='zip_code')
# Ensure all expected columns are present even if some zip codes are missing
for col in ['zip_code_10001', 'zip_code_20002', 'zip_code_30003', 'zip_code_40004']:
    if col not in dummies.columns:
        dummies[col] = 0

df = pd.concat([df, dummies], axis=1)

features = ['month', 'price', 'marketing_spend', 'zip_code_10001', 'zip_code_20002', 'zip_code_30003', 'zip_code_40004']
X = df[features]
y = df['sales']

model = Ridge(alpha=1.0, random_state=42)
model.fit(X, y)
preds = model.predict(X)

mse = mean_squared_error(y, preds)
print(f"{mse:.2f}")
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to compute expected MSE: {result.stderr}")
    return result.stdout.strip()

def test_predictions_file_exists():
    assert os.path.isfile(PREDICTIONS_FILE), f"The file {PREDICTIONS_FILE} was not generated."

def test_metrics_file_exists():
    assert os.path.isfile(METRICS_FILE), f"The file {METRICS_FILE} was not generated."

def test_predictions_format_and_count():
    assert os.path.isfile(PREDICTIONS_FILE), f"Missing {PREDICTIONS_FILE}"

    with open(PREDICTIONS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['id', 'predicted_sales'], f"Header in {PREDICTIONS_FILE} is incorrect. Expected ['id', 'predicted_sales'], got {header}"

        rows = list(reader)
        assert len(rows) == 500, f"Expected 500 prediction rows, but found {len(rows)}."

        for i, row in enumerate(rows):
            assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns."
            try:
                int(row[0])
                float(row[1])
            except ValueError:
                pytest.fail(f"Row {i+1} contains invalid data types: {row}")

def test_metrics_content():
    assert os.path.isfile(METRICS_FILE), f"Missing {METRICS_FILE}"

    with open(METRICS_FILE, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content.startswith("MSE: "), f"{METRICS_FILE} does not start with 'MSE: '"

    expected_mse = get_expected_mse()
    expected_content = f"MSE: {expected_mse}"

    assert content == expected_content, f"Metrics file content is incorrect. Expected '{expected_content}', got '{content}'."