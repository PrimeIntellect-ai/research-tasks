# test_final_state.py

import os
import json
import math
import pytest
import requests

def test_cleaned_dataset():
    cleaned_path = "/home/user/data/cleaned_dataset.csv"
    assert os.path.exists(cleaned_path), f"Cleaned dataset not found at {cleaned_path}"

    with open(cleaned_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 5, "Cleaned dataset should have header and 4 data rows"

    header = lines[0]
    assert "user_id" in header
    assert "age" in header
    assert "amount" in header

    # Verify user 3 is dropped
    for line in lines[1:]:
        assert not line.startswith("3,"), "User 3 should have been dropped due to missing age."

def test_experiment_log():
    log_path = "/home/user/experiment_log.json"
    assert os.path.exists(log_path), f"Experiment log not found at {log_path}"

    with open(log_path, "r") as f:
        data = json.load(f)

    assert "mean_amount" in data, "Missing 'mean_amount' in experiment log"
    assert "correlation_age_amount" in data, "Missing 'correlation_age_amount' in experiment log"

    assert math.isclose(data["mean_amount"], 75.375, rel_tol=1e-3), f"Expected mean_amount ~75.375, got {data['mean_amount']}"

    # Accept a wide range due to potential differences in correlation computation (sample vs population, etc.)
    corr = data["correlation_age_amount"]
    assert -0.95 <= corr <= -0.75, f"Expected correlation_age_amount to be around -0.8, got {corr}"

def test_api_stats_unauthorized():
    url = "http://0.0.0.0:8888/api/stats"
    try:
        resp = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized without auth header, got {resp.status_code}"

def test_api_stats_authorized():
    url = "http://0.0.0.0:8888/api/stats"
    headers = {"Authorization": "Bearer ds-secret"}
    try:
        resp = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {resp.text}")

    assert "mean_amount" in data, "Missing 'mean_amount' in API response"
    assert "correlation_age_amount" in data, "Missing 'correlation_age_amount' in API response"
    assert math.isclose(data["mean_amount"], 75.375, rel_tol=1e-3), "Incorrect mean_amount in API response"

def test_api_data_authorized():
    url = "http://0.0.0.0:8888/api/data"
    headers = {"Authorization": "Bearer ds-secret"}
    try:
        resp = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {resp.text}")

    assert isinstance(data, list), "Expected API to return a list of dictionaries"
    assert len(data) > 0, "API returned empty list"

    # Check that it's a list of dicts with correct keys
    first_row = data[0]
    assert isinstance(first_row, dict), "Expected list of dictionaries"
    assert "user_id" in first_row, "Missing 'user_id' in API data"
    assert "amount" in first_row, "Missing 'amount' in API data"