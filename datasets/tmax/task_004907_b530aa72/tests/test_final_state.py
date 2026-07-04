# test_final_state.py

import json
import math
import pytest
import requests

URL = "http://127.0.0.1:8000/process"
AUTH_HEADER = {"Authorization": "Bearer ds-secret-token"}

CSV_CONTENT = """patient_id,age,weight
101,25,70.5
102,,80.0
103,40,
"""

def test_missing_auth():
    """Test that requests without the Authorization header return 401."""
    files = {"dataset": ("dataset.csv", CSV_CONTENT, "text/csv")}
    try:
        response = requests.post(URL, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {response.status_code}"

def test_invalid_auth():
    """Test that requests with an invalid Authorization header return 401."""
    files = {"dataset": ("dataset.csv", CSV_CONTENT, "text/csv")}
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.post(URL, headers=headers, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid auth, got {response.status_code}"

def test_process_dataset():
    """Test that a valid request processes the dataset correctly."""
    files = {"dataset": ("dataset.csv", CSV_CONTENT, "text/csv")}
    try:
        response = requests.post(URL, headers=AUTH_HEADER, files=files, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    assert isinstance(data, list), "Expected response to be a JSON array"
    assert len(data) == 3, f"Expected 3 records, got {len(data)}"

    # Check first record
    r1 = data[0]
    assert r1.get("patient_id") == 101
    assert type(r1.get("patient_id")) is int, "patient_id must be an integer"
    assert r1.get("age") == 25
    assert type(r1.get("age")) is int, "age must be an integer"
    assert math.isclose(r1.get("weight"), 70.5, rel_tol=1e-5)
    assert math.isclose(r1.get("proj_1"), -1.6, rel_tol=1e-5)
    assert math.isclose(r1.get("proj_2"), 27.05, rel_tol=1e-5)

    # Check second record
    r2 = data[1]
    assert r2.get("patient_id") == 102
    assert r2.get("age") is None, "Missing age must be represented as null"
    assert math.isclose(r2.get("weight"), 80.0, rel_tol=1e-5)
    assert math.isclose(r2.get("proj_1"), -16.0, rel_tol=1e-5)
    assert math.isclose(r2.get("proj_2"), 8.0, rel_tol=1e-5)

    # Check third record
    r3 = data[2]
    assert r3.get("patient_id") == 103
    assert r3.get("age") == 40
    assert type(r3.get("age")) is int, "age must be an integer"
    assert r3.get("weight") is None, "Missing weight must be represented as null"
    assert math.isclose(r3.get("proj_1"), 20.0, rel_tol=1e-5)
    assert math.isclose(r3.get("proj_2"), 32.0, rel_tol=1e-5)