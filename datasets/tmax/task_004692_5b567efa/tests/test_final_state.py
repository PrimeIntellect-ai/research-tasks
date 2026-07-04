# test_final_state.py

import os
import json
import math
import subprocess
import sys
import pytest

def get_expected_metrics():
    """
    Computes the expected metrics by running the golden logic in a subprocess.
    This avoids directly importing third-party libraries in the pytest file,
    while still dynamically computing the expected values based on the data.
    """
    script = """
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json

df = pd.read_csv('/home/user/data/raw.csv')
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)
preds = model.predict(X_test_scaled)

expected_accuracy = accuracy_score(y_test, preds)
expected_f0_mean = float(np.mean(X_test_scaled[:, 0]))

print(json.dumps({'accuracy': expected_accuracy, 'test_feature_0_mean': expected_f0_mean}))
"""
    try:
        result = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected metrics. Error: {e.stderr}")

def test_metrics_file_exists():
    assert os.path.isfile('/home/user/metrics.json'), "The file /home/user/metrics.json does not exist."

def test_metrics_correctness():
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"Metrics file missing at {metrics_path}"

    with open(metrics_path, 'r') as f:
        try:
            actual_metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/metrics.json does not contain valid JSON.")

    assert 'accuracy' in actual_metrics, "The 'accuracy' key is missing from metrics.json."
    assert 'test_feature_0_mean' in actual_metrics, "The 'test_feature_0_mean' key is missing from metrics.json."

    expected_metrics = get_expected_metrics()

    actual_accuracy = actual_metrics['accuracy']
    expected_accuracy = expected_metrics['accuracy']
    assert math.isclose(actual_accuracy, expected_accuracy, rel_tol=1e-5, abs_tol=1e-5), \
        f"Accuracy is incorrect. Expected {expected_accuracy}, got {actual_accuracy}. The data leakage bug might not be fully resolved."

    actual_f0_mean = actual_metrics['test_feature_0_mean']
    expected_f0_mean = expected_metrics['test_feature_0_mean']
    assert math.isclose(actual_f0_mean, expected_f0_mean, rel_tol=1e-5, abs_tol=1e-5), \
        f"Test feature 0 mean is incorrect. Expected {expected_f0_mean}, got {actual_f0_mean}. Ensure transformers are fitted ONLY on the training data."