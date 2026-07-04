# test_final_state.py

import os
import json
import subprocess
import sys
import pytest

def get_expected_accuracy():
    """
    Computes the expected accuracy by running the canonical operations in a subprocess.
    This avoids importing third-party libraries directly in the test file.
    """
    script = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

users = pd.read_csv('/home/user/data/users.csv')
tx = pd.read_csv('/home/user/data/transactions.csv')
df = pd.merge(tx, users, on='user_id')

# Schema enforcement
df = df.dropna(subset=['age'])
df = df[df['amount'] >= 0]

X = df[['amount', 'age', 'location_id']]
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fix Leakage
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[['amount', 'age']] = scaler.fit_transform(X_train[['amount', 'age']])
X_test_scaled[['amount', 'age']] = scaler.transform(X_test[['amount', 'age']])

model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)
expected_accuracy = model.score(X_test_scaled, y_test)
print(expected_accuracy)
"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected accuracy. Subprocess error: {e.stderr}")

def test_metrics_file_exists_and_valid():
    """Check that the metrics file exists and contains valid JSON with the 'accuracy' key."""
    metrics_file = '/home/user/metrics_fixed.json'
    assert os.path.isfile(metrics_file), f"The file {metrics_file} was not created."

    with open(metrics_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {metrics_file} does not contain valid JSON.")

    assert "accuracy" in data, f"The JSON in {metrics_file} is missing the 'accuracy' key."
    assert isinstance(data["accuracy"], (int, float)), "The 'accuracy' value must be a number."

def test_correct_accuracy():
    """Check that the accuracy matches the expected value after fixing schema and leakage."""
    metrics_file = '/home/user/metrics_fixed.json'
    if not os.path.isfile(metrics_file):
        pytest.fail(f"Cannot check accuracy because {metrics_file} is missing.")

    with open(metrics_file, 'r') as f:
        data = json.load(f)

    actual_accuracy = data.get("accuracy")
    expected_accuracy = get_expected_accuracy()

    # We use a small tolerance for floating point comparisons
    tolerance = 1e-7
    diff = abs(actual_accuracy - expected_accuracy)

    assert diff < tolerance, (
        f"The reported accuracy ({actual_accuracy}) does not match the expected accuracy "
        f"({expected_accuracy}). Ensure schema enforcement and leakage fixes are correct."
    )