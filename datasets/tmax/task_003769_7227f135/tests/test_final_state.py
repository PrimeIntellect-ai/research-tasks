# test_final_state.py

import os
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
API_KEY = "X88-912-SYS-AUTH"

def test_recovered_db_exists():
    path = "/app/data/metrics_recovered.db"
    assert os.path.isfile(path), f"Expected recovered database at {path}."

def test_health_endpoint_and_bug_fix():
    # Make 5 requests to ensure the intermittent bug (crash on 4th request) is fixed
    for i in range(1, 6):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
        except requests.exceptions.ConnectionError:
            pytest.fail(f"Failed to connect to the API server at {BASE_URL}. Is it running?")
        except requests.exceptions.Timeout:
            pytest.fail(f"Request to {BASE_URL}/health timed out.")

        assert response.status_code == 200, f"Expected status code 200 on request {i}, got {response.status_code}"
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Expected JSON response from /health, got: {response.text}")

        assert data == {"status": "ok"}, f"Expected {{'status': 'ok'}} on request {i}, got {data}"

def test_metrics_unauthorized():
    try:
        response = requests.get(f"{BASE_URL}/metrics/db-node-01", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code in (401, 403), f"Expected status code 401 or 403 for unauthorized request, got {response.status_code}"

def test_metrics_authorized():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(f"{BASE_URL}/metrics/db-node-01", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected status code 200 for authorized request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /metrics/db-node-01, got: {response.text}")

    assert data.get("hostname") == "db-node-01", f"Expected hostname 'db-node-01', got {data.get('hostname')}"

    # Use a small tolerance for floating point comparison, or exact match if it's strictly 99.98
    uptime = data.get("uptime")
    assert uptime is not None, "Response missing 'uptime' field."
    assert abs(float(uptime) - 99.98) < 0.001, f"Expected uptime ~99.98, got {uptime}"