# test_final_state.py

import pytest
import requests
import math

def test_metrics_endpoint():
    url = "http://127.0.0.1:8080/metrics"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_keys = {
        "alpha_values",
        "beta_values",
        "t_test_p_value",
        "bayesian_posterior_mean",
        "bayesian_ci_lower",
        "bayesian_ci_upper"
    }

    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"JSON response is missing required keys: {missing_keys}"

    # Check extracted values
    # Depending on the transcription model, there might be slight variations, but for synthesized clear audio,
    # it usually matches exactly. We check with a small tolerance.
    expected_alpha = [22.5, 23.1, 22.8]
    expected_beta = [21.0, 20.8, 21.2]

    assert len(data["alpha_values"]) == len(expected_alpha), "Incorrect number of alpha values extracted."
    assert len(data["beta_values"]) == len(expected_beta), "Incorrect number of beta values extracted."

    for act, exp in zip(data["alpha_values"], expected_alpha):
        assert math.isclose(act, exp, abs_tol=0.1), f"Alpha value {act} does not match expected {exp}"

    for act, exp in zip(data["beta_values"], expected_beta):
        assert math.isclose(act, exp, abs_tol=0.1), f"Beta value {act} does not match expected {exp}"

    # Check calculated statistics with a reasonable tolerance
    # (Allowing for slight variations in rounding or exact z-score/t-score used)
    assert math.isclose(data["t_test_p_value"], 0.003, abs_tol=0.005), \
        f"t_test_p_value {data['t_test_p_value']} is not close to expected 0.003"

    assert math.isclose(data["bayesian_posterior_mean"], 22.763, abs_tol=0.01), \
        f"bayesian_posterior_mean {data['bayesian_posterior_mean']} is not close to expected 22.763"

    assert math.isclose(data["bayesian_ci_lower"], 21.639, abs_tol=0.05), \
        f"bayesian_ci_lower {data['bayesian_ci_lower']} is not close to expected 21.639"

    assert math.isclose(data["bayesian_ci_upper"], 23.887, abs_tol=0.05), \
        f"bayesian_ci_upper {data['bayesian_ci_upper']} is not close to expected 23.887"