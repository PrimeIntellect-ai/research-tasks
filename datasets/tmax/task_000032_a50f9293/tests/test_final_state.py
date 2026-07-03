# test_final_state.py

import pytest
import requests
import time

def test_api_calculates_correct_roots():
    url = "http://localhost:8080/calculate"
    payload = {"audio_path": "/app/incident report 01.wav"}

    # Allow a brief moment in case the service is still starting
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=2)
            break
        except requests.exceptions.RequestException as e:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to the API on port 8080: {e}")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "roots" in data, f"Response JSON missing 'roots' key. Got: {data}"

    roots = data["roots"]
    assert isinstance(roots, list), f"Expected 'roots' to be a list, got {type(roots)}"

    # The truth roots for the provided audio file "a equals one, b equals zero, c equals negative four."
    # x^2 - 4 = 0 => x = -2.0, 2.0
    expected_roots = [-2.0, 2.0]

    assert len(roots) == 2, f"Expected 2 roots, got {len(roots)}: {roots}"

    # Sort roots to ensure ascending order as per task description
    sorted_roots = sorted(roots)

    # Allow for minor floating point inaccuracies
    assert abs(sorted_roots[0] - expected_roots[0]) < 1e-5, f"First root incorrect. Expected {expected_roots[0]}, got {sorted_roots[0]}"
    assert abs(sorted_roots[1] - expected_roots[1]) < 1e-5, f"Second root incorrect. Expected {expected_roots[1]}, got {sorted_roots[1]}"