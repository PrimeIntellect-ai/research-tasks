# test_final_state.py

import math
import requests
import pytest

def test_api_analyze_endpoint():
    """
    Test the /analyze endpoint of the API service.
    It should accept a sequence, calculate the correct original_energy,
    and return a valid p_value.
    """
    url = "http://127.0.0.1:8000/analyze"
    payload = {"sequence": "MASGY"}

    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "original_energy" in data, f"Missing 'original_energy' in response JSON: {data}"
    assert "p_value" in data, f"Missing 'p_value' in response JSON: {data}"

    # Check original energy for MASGY
    # M-A: |149-89|*(1.9+1.8) = 60 * 3.7 = 222.0
    # A-S: |89-105|*(1.8 - 0.8) = 16 * 1.0 = 16.0
    # S-G: |105-75|*(-0.8 - 0.4) = 30 * -1.2 = -36.0
    # G-Y: |75-181|*(-0.4 - 1.3) = 106 * -1.7 = -180.2
    # Total E = 222 + 16 - 36 - 180.2 = 21.8
    expected_energy = 21.8
    actual_energy = data["original_energy"]
    assert isinstance(actual_energy, (int, float)), "original_energy must be a number"
    assert math.isclose(actual_energy, expected_energy, abs_tol=0.1), \
        f"Expected original_energy to be approximately {expected_energy}, got {actual_energy}"

    # Check p_value
    p_val = data["p_value"]
    assert isinstance(p_val, (int, float)), "p_value must be a number"
    assert 0.0 <= p_val <= 1.0, f"p_value must be between 0.0 and 1.0, got {p_val}"