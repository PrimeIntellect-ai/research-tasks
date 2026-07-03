# test_final_state.py

import math
import requests
import pytest

def test_api_report():
    url = "http://127.0.0.1:8080/api/report"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}. Response text: {response.text}")

    assert "energy" in data, f"JSON response missing 'energy' key. Keys found: {list(data.keys())}"
    assert "dominant_freq" in data, f"JSON response missing 'dominant_freq' key. Keys found: {list(data.keys())}"

    # Compute expected energy deterministically
    N = 10000
    DT = 0.001
    f0 = 50.0
    decay = 0.02
    expected_energy = 0.0
    for i in range(N):
        t = i * DT
        val = math.exp(-decay * t) * math.sin(2 * math.pi * f0 * t)
        expected_energy += abs(val)

    try:
        actual_energy = float(data["energy"])
    except ValueError:
        pytest.fail(f"Could not convert 'energy' to float. Value: {data['energy']}")

    try:
        actual_freq = float(data["dominant_freq"])
    except ValueError:
        pytest.fail(f"Could not convert 'dominant_freq' to float. Value: {data['dominant_freq']}")

    assert math.isclose(actual_freq, 50.0, rel_tol=1e-3), f"Expected dominant_freq to be ~50.0, got {actual_freq}"
    assert math.isclose(actual_energy, expected_energy, rel_tol=1e-5), f"Expected energy to be ~{expected_energy}, got {actual_energy}"