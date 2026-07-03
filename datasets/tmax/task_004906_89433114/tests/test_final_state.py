# test_final_state.py

import os
import pytest
import requests
import time

def test_serve_model_script_exists():
    """Verify that the agent created the required script."""
    script_path = "/home/user/serve_model.py"
    assert os.path.exists(script_path), f"Expected script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_flask_service_predict_endpoint():
    """Verify the Flask service is running and returns the correct prediction."""
    url = "http://127.0.0.1:5050/predict"
    params = {"views": 1000}

    # Try to connect with retries in case the service is slow to start
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail("Failed to connect to the Flask service on 127.0.0.1:5050. Is it running?")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "expected_clicks" in data, f"JSON response missing 'expected_clicks' key. Got: {data}"

    expected_clicks = data["expected_clicks"]
    assert isinstance(expected_clicks, (int, float)), f"'expected_clicks' should be a number, got {type(expected_clicks)}"

    # The true relationship is clicks = 0.15 * views. For views=1000, expected clicks is 150.
    assert 149.0 <= expected_clicks <= 151.0, f"Expected prediction around 150.0, but got {expected_clicks}"