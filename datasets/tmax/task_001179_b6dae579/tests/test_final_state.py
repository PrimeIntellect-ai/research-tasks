# test_final_state.py

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_service():
    """Wait for the web service to become available."""
    for _ in range(10):
        try:
            # Just test connection
            requests.get(BASE_URL, timeout=1)
            return True
        except requests.RequestException:
            time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_service_running():
    # We don't strictly assert here, we let the individual tests fail if it's down,
    # but waiting helps if it's slow to respond.
    wait_for_service()

def test_evaluate_simple():
    """Test POST /evaluate with a simple RPN expression."""
    payload = {"expression": "10 20 + 30 *"}
    try:
        response = requests.post(f"{BASE_URL}/evaluate", json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect or request timed out: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 900, f"Expected result 900, got {data['result']}"

def test_evaluate_large():
    """Test POST /evaluate with a large RPN expression to check for overflows."""
    expression = " ".join(["1"] * 1000 + ["+"] * 999)
    payload = {"expression": expression}
    try:
        response = requests.post(f"{BASE_URL}/evaluate", json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect or request timed out: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 1000, f"Expected result 1000, got {data['result']}"

def test_evaluate_image():
    """Test GET /image which runs OCR and evaluates the resulting expression."""
    try:
        response = requests.get(f"{BASE_URL}/image", timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect or request timed out: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 80, f"Expected result 80, got {data['result']}"