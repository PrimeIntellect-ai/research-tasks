# test_final_state.py

import json
import math
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"

def test_montecarlo_endpoint():
    url = f"{BASE_URL}/montecarlo?samples=1000000"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    assert "mc_prob" in data, f"Key 'mc_prob' missing in response. Got: {data}"

    mc_prob = data["mc_prob"]
    assert isinstance(mc_prob, (int, float)), f"'mc_prob' must be a number, got {type(mc_prob)}"

    expected_prob = 0.02275
    tolerance = 0.005
    assert abs(mc_prob - expected_prob) <= tolerance, f"Expected 'mc_prob' to be around {expected_prob} (+/- {tolerance}), but got {mc_prob}"

def test_integrate_endpoint():
    url = f"{BASE_URL}/integrate"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    assert "exact_prob" in data, f"Key 'exact_prob' missing in response. Got: {data}"

    exact_prob = data["exact_prob"]
    assert isinstance(exact_prob, (int, float)), f"'exact_prob' must be a number, got {type(exact_prob)}"

    # Calculate exact prob: P(X > 180) for N(120, 30) = P(Z > 2)
    # Using math.erfc(2 / sqrt(2)) / 2
    expected_exact_prob = math.erfc(2.0 / math.sqrt(2.0)) / 2.0
    tolerance = 0.0001

    assert abs(exact_prob - expected_exact_prob) <= tolerance, f"Expected 'exact_prob' to be around {expected_exact_prob} (+/- {tolerance}), but got {exact_prob}"

def test_test_endpoint():
    url = f"{BASE_URL}/test"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    assert "z_score" in data, f"Key 'z_score' missing in response. Got: {data}"

    z_score = data["z_score"]
    assert isinstance(z_score, (int, float)), f"'z_score' must be a number, got {type(z_score)}"

    # Calculate expected z-score based on the profiling_data.csv
    # Sample mean is exactly 126.5, N=100, mu=120, sigma=30
    expected_z_score = (126.5 - 120.0) / (30.0 / math.sqrt(100))
    tolerance = 0.001

    assert abs(z_score - expected_z_score) <= tolerance, f"Expected 'z_score' to be around {expected_z_score} (+/- {tolerance}), but got {z_score}"