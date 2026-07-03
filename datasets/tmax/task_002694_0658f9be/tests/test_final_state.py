# test_final_state.py

import os
import csv
import requests
import pytest

API_URL = "http://127.0.0.1:8000/predict"
AUTH_HEADER = {"Authorization": "Bearer secret-ds-token-8819"}

def test_pyjanitor_bug_fixed():
    """Verify that the deliberate bug in pyjanitor has been removed."""
    filepath = "/app/pyjanitor/janitor/functions/fill.py"
    assert os.path.exists(filepath), f"File {filepath} not found."
    with open(filepath, "r") as f:
        content = f.read()

    # Check that the specific bug line is removed
    assert "df.loc[df[column_name].isna(), column_name] = np.nan" not in content, \
        "The deliberate bug in pyjanitor's fill_empty function is still present."

def test_api_missing_auth():
    """Verify that the API rejects requests without the auth header."""
    try:
        response = requests.post(API_URL, json={"dummy": 1}, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API server on port 8000.")

    assert response.status_code in (401, 403), \
        f"Expected 401 or 403 for missing auth, got {response.status_code}"

def test_api_invalid_auth():
    """Verify that the API rejects requests with an invalid auth header."""
    headers = {"Authorization": "Bearer wrong-token-123"}
    try:
        response = requests.post(API_URL, headers=headers, json={"dummy": 1}, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API server on port 8000.")

    assert response.status_code in (401, 403), \
        f"Expected 401 or 403 for invalid auth, got {response.status_code}"

def test_api_prediction_endpoint():
    """Verify that the API returns correctly formatted predictions for a valid request."""
    # Read the first row of the training data to get realistic feature names
    data_path = "/home/user/train_data.csv"
    assert os.path.exists(data_path), f"Dataset {data_path} is missing."

    with open(data_path, "r") as f:
        reader = csv.DictReader(f)
        row = next(reader)

    # Prepare features (fill missing with 0 as per instructions)
    features = {}
    for k, v in row.items():
        if k != "target":
            try:
                features[k] = float(v) if v.strip() else 0.0
            except ValueError:
                features[k] = 0.0

    try:
        response = requests.post(API_URL, headers=AUTH_HEADER, json=features, timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API server on port 8000.")

    assert response.status_code == 200, \
        f"Expected 200 OK for valid request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "mean_prediction" in data, "Response JSON is missing 'mean_prediction' key."
    assert "uncertainty" in data, "Response JSON is missing 'uncertainty' key."

    assert isinstance(data["mean_prediction"], (int, float)), \
        f"'mean_prediction' should be a float, got {type(data['mean_prediction'])}"
    assert isinstance(data["uncertainty"], (int, float)), \
        f"'uncertainty' should be a float, got {type(data['uncertainty'])}"