# test_final_state.py

import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8050"

def rk4_step(I, r, K, h):
    k1 = r * I * (1 - I / K)
    k2 = r * (I + 0.5 * h * k1) * (1 - (I + 0.5 * h * k1) / K)
    k3 = r * (I + 0.5 * h * k2) * (1 - (I + 0.5 * h * k2) / K)
    k4 = r * (I + h * k3) * (1 - (I + h * k3) / K)
    return I + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def simulate_rk4(r, K, I0, t, h=0.01):
    steps = int(round(t / h))
    I = I0
    for _ in range(steps):
        I = rk4_step(I, r, K, h)
    return I

def test_fit_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/fit", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /fit endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /fit is not valid JSON: {response.text}")

    assert "r" in data, "Missing 'r' in /fit response"
    assert "K" in data, "Missing 'K' in /fit response"

    r_val = float(data["r"])
    K_val = float(data["K"])

    assert abs(r_val - 1.200) <= 0.05, f"Fitted 'r' ({r_val}) is outside acceptable range [1.15, 1.25]"
    assert abs(K_val - 200.000) <= 2.0, f"Fitted 'K' ({K_val}) is outside acceptable range [198.0, 202.0]"

@pytest.mark.parametrize("t_val", [3.5, 8.2])
def test_simulate_endpoint(t_val):
    # Get the agent's fitted parameters first to calculate expected I
    try:
        fit_response = requests.get(f"{BASE_URL}/fit", timeout=5)
        fit_data = fit_response.json()
        r_val = float(fit_data["r"])
        K_val = float(fit_data["K"])
    except Exception as e:
        pytest.fail(f"Could not retrieve parameters from /fit for simulation test: {e}")

    expected_I = simulate_rk4(r_val, K_val, 15.0, t_val, h=0.01)

    try:
        response = requests.get(f"{BASE_URL}/simulate?t={t_val}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /simulate endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200 for /simulate?t={t_val}, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /simulate is not valid JSON: {response.text}")

    assert "I" in data, "Missing 'I' in /simulate response"

    I_val = float(data["I"])

    assert abs(I_val - expected_I) <= 0.1, f"Simulated 'I' ({I_val}) at t={t_val} does not match expected RK4 result ({expected_I}) within 0.1 margin"