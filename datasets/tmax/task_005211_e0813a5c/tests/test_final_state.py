# test_final_state.py

import os
import sys
import json
import pytest
import requests
import pandas as pd

def test_datacleaner_bug_fixed():
    """Test that the datacleaner package drops invalid age rows."""
    # Ensure we can import it even if not installed globally
    sys.path.insert(0, "/app/datacleaner-1.2.0")
    try:
        from datacleaner.schema import enforce_age_schema
    except ImportError:
        pytest.fail("Could not import datacleaner.schema. Was the package installed/fixed?")

    df = pd.DataFrame({
        "age": ["25", "twenty", "30"],
        "income": [50000.0, 60000.0, 70000.0],
        "category": ["A", "B", "A"]
    })

    try:
        cleaned_df = enforce_age_schema(df)
    except Exception as e:
        pytest.fail(f"enforce_age_schema raised an exception: {e}")

    assert len(cleaned_df) == 2, "Expected rows with invalid age ('twenty') to be dropped."
    assert cleaned_df["age"].isna().sum() == 0, "Expected no NaN values in the age column."

def test_benchmark_results_exists():
    """Test that the benchmark results file was created."""
    benchmark_file = "/home/user/benchmark_results.txt"
    assert os.path.isfile(benchmark_file), f"Benchmark results file {benchmark_file} is missing."
    with open(benchmark_file, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, "Benchmark results file is empty."

def test_predict_endpoint_auth():
    """Test that the endpoint requires authorization."""
    url = "http://127.0.0.1:8000/predict"
    payload = {"data": [{"age": "25", "income": 50000.0, "category": "A"}]}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the prediction service: {e}")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for missing auth, got {response.status_code}"

def test_predict_endpoint_success():
    """Test that the endpoint returns predictions with valid auth and payload."""
    url = "http://127.0.0.1:8000/predict"
    headers = {"Authorization": "Bearer secret-token-99X"}
    payload = {
        "data": [
            {"age": "25", "income": 50000.0, "category": "A"},
            {"age": "35", "income": 80000.0, "category": "B"}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the prediction service: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "predictions" in data, "Response JSON is missing the 'predictions' key."
    predictions = data["predictions"]
    assert isinstance(predictions, list), "Expected 'predictions' to be a list."
    assert len(predictions) > 0, "Expected at least one prediction in the list."