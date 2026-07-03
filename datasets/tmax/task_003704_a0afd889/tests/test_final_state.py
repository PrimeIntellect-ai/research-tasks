# test_final_state.py

import os
import requests
import pytest

APP_DIR = "/home/user/app"
BASE_URL = "http://127.0.0.1:8080"
API_SECRET = "git-sec-9942x"

def test_health_endpoint():
    """Verify the health endpoint returns 200 OK and the correct status."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the FastAPI frontend on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert data.get("status") == "healthy", f"Expected status 'healthy', got {data.get('status')}"

def test_secure_data_endpoint():
    """Verify the secure-data endpoint returns the correct payload from Redis using the recovered API secret."""
    headers = {
        "Authorization": f"Bearer {API_SECRET}"
    }

    try:
        response = requests.get(f"{BASE_URL}/secure-data", headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the FastAPI frontend on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert data.get("data") == "secret-payload-from-redis", f"Expected data 'secret-payload-from-redis', got {data.get('data')}"

def test_debugging_report_exists():
    """Verify that the student has written a debugging report."""
    report_path = os.path.join(APP_DIR, "debugging_report.txt")
    assert os.path.isfile(report_path), f"Debugging report not found at {report_path}"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert len(content) > 0, f"Debugging report at {report_path} is empty."