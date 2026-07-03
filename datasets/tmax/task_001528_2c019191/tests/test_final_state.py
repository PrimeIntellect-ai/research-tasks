# test_final_state.py

import pytest
import requests
import time

PORT = 9090
URL = f"http://127.0.0.1:{PORT}/"
TOKEN = "PERF_BASH_88X"

def wait_for_service():
    """Wait for the socat service to be available."""
    for _ in range(10):
        try:
            requests.get(URL, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
        except requests.exceptions.ReadTimeout:
            # If it times out, it might be up but not responding properly, which is fine for the check
            return True
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_service_up():
    assert wait_for_service(), f"Service is not listening on port {PORT}."

def test_no_auth_returns_401():
    try:
        response = requests.get(URL, timeout=2)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth, got {response.status_code}"

def test_invalid_auth_returns_401():
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    try:
        response = requests.get(URL, headers=headers, timeout=2)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with invalid auth, got {response.status_code}"

def test_valid_auth_and_payload_returns_correct_average():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = "/login,45ms\n/home, 120 ms\n/api/data,85.5\n/api/data, 100"

    try:
        response = requests.post(URL, headers=headers, data=payload, timeout=2)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "average" in data, "JSON response missing 'average' key"
    assert data["average"] == 88, f"Expected average to be 88, got {data['average']}"

def test_valid_auth_and_different_payload():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = "/a,10\n/b, 20.4 \n/c,30 ms"

    try:
        response = requests.post(URL, headers=headers, data=payload, timeout=2)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "average" in data, "JSON response missing 'average' key"
    assert data["average"] == 20, f"Expected average to be 20, got {data['average']}"