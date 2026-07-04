# test_final_state.py

import pytest
import requests
import random
import time

def test_api_polycalc():
    """
    Test the Bash HTTP server by sending multiple sequential POST requests
    and verifying the calculated result.
    """
    url = "http://127.0.0.1:8080/api/v1/math/poly"

    # Wait a brief moment to ensure the server is up (if started recently)
    time.sleep(1)

    for _ in range(5):
        x = random.randint(1, 20)
        y = random.randint(1, 20)
        payload = {"x": x, "y": y}
        expected_result = 3 * (x ** 2) + 2 * y + 1

        try:
            response = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request to {url} failed: {e}")

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "status" in data, f"Missing 'status' in response: {data}"
        assert data["status"] == "success", f"Expected status 'success', got {data['status']}"
        assert "result" in data, f"Missing 'result' in response: {data}"
        assert data["result"] == expected_result, f"For x={x}, y={y}, expected result {expected_result}, got {data['result']}"