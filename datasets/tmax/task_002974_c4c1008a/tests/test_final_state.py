# test_final_state.py

import pytest
import requests
import time
import math

def test_server_is_running_and_responds_correctly():
    url = "http://127.0.0.1:9090/zeta"
    params = {"iter": 5, "val": 2.0}

    # Try to connect with a few retries in case the server is slow to respond
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail("Failed to connect to the server at 127.0.0.1:9090. Is it running?")
            time.sleep(1)

    assert response is not None
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response text: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "result" in data, f"JSON response missing 'result' key. Response data: {data}"

    expected_result = 3.603825625
    actual_result = data["result"]

    assert isinstance(actual_result, (int, float)), f"'result' must be a number, got {type(actual_result)}"
    assert math.isclose(actual_result, expected_result, rel_tol=1e-5), f"Expected result ~{expected_result}, got {actual_result}"