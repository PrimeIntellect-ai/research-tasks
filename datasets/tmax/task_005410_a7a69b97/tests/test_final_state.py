# test_final_state.py

import pytest
import requests
import json
import os

BASE_URL = "http://127.0.0.1:9090"
TOKEN = "iron_badger"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_missing_auth():
    """Test that requests without the Authorization header return 401."""
    try:
        response = requests.get(f"{BASE_URL}/lineage?id=B-005", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:9090")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_invalid_auth():
    """Test that requests with an incorrect Authorization header return 401."""
    try:
        response = requests.get(f"{BASE_URL}/lineage?id=B-005", headers={"Authorization": "Bearer wrong_token"}, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:9090")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}"

def test_valid_request_lineage():
    """Test that a valid request returns the correct lineage, sorted by timestamp."""
    try:
        response = requests.get(f"{BASE_URL}/lineage?id=B-005", headers=HEADERS, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:9090")

    assert response.status_code == 200, f"Expected HTTP 200 for valid request, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "lineage" in data, "Response JSON is missing 'lineage' key"
    expected_lineage = ["B-001", "B-002", "B-003", "B-004", "B-005"]
    assert data["lineage"] == expected_lineage, f"Expected lineage {expected_lineage}, got {data['lineage']}"

def test_nonexistent_id():
    """Test that requesting a non-existent ID returns 404."""
    try:
        response = requests.get(f"{BASE_URL}/lineage?id=NON_EXISTENT", headers=HEADERS, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:9090")

    assert response.status_code == 404, f"Expected HTTP 404 for non-existent ID, got {response.status_code}"