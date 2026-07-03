# test_final_state.py
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"

def test_evaluate_linear():
    url = f"{BASE_URL}/evaluate"
    payload = {"expression": "3 * x + 5", "x_value": 2.0}

    for _ in range(10):
        try:
            response = requests.post(url, json=payload, timeout=2)
            break
        except requests.RequestException:
            time.sleep(1)
    else:
        pytest.fail("Server is not running or not reachable at 127.0.0.1:8080")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Body: {data}"
    assert abs(data["result"] - 11.0) < 1e-5, f"Expected result ~11.0, got {data['result']}"

def test_evaluate_trig():
    url = f"{BASE_URL}/evaluate"
    payload = {"expression": "sin(x) * cos(x)", "x_value": 0.0}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Body: {data}"
    assert abs(data["result"] - 0.0) < 1e-5, f"Expected result ~0.0, got {data['result']}"

def test_evaluate_invalid():
    url = f"{BASE_URL}/evaluate"
    payload = {"expression": "invalid_syntax++", "x_value": 1.0}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {response.text}")

    assert "error" in data, f"Response JSON missing 'error' key. Body: {data}"
    assert data["error"] == "Invalid expression", f"Expected error message 'Invalid expression', got '{data['error']}'"