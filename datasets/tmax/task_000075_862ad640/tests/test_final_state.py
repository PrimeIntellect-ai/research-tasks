# test_final_state.py

import pytest
import requests
import time

def test_metrics_endpoint():
    """
    Check that the server is running on 127.0.0.1:8080/metrics,
    returns a JSON response with the required keys, and the values
    are within the expected statistical bounds.
    """
    url = "http://127.0.0.1:8080/metrics"

    # Retry a few times in case the server is slow to start
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to the server at {url}. Is it running?")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    required_keys = {"wasserstein", "ci_lower", "ci_upper"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in JSON response: {missing_keys}"

    wasserstein = float(data["wasserstein"])
    ci_lower = float(data["ci_lower"])
    ci_upper = float(data["ci_upper"])

    assert 0.45 <= wasserstein <= 0.55, f"Wasserstein distance {wasserstein} is out of expected range [0.45, 0.55]"
    assert 0.40 <= ci_lower <= 0.50, f"CI lower bound {ci_lower} is out of expected range [0.40, 0.50]"
    assert 0.50 <= ci_upper <= 0.60, f"CI upper bound {ci_upper} is out of expected range [0.50, 0.60]"

    assert ci_lower < wasserstein < ci_upper, f"Expected ci_lower < wasserstein < ci_upper, but got {ci_lower} < {wasserstein} < {ci_upper}"