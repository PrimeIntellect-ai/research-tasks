# test_final_state.py

import pytest
import requests
import math

def test_pricing_service_success():
    """Verify the pricing service returns the correct double-precision result."""
    url = "http://127.0.0.1:8080/price"
    params = {"s": "123456789.0"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the pricing service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        result = float(response.text)
    except ValueError:
        pytest.fail(f"Failed to parse response body as a float: {response.text}")

    expected = 11111.111060555555
    assert abs(result - expected) < 1e-7, (
        f"Expected result close to {expected}, but got {result}. "
        "This likely means the algorithm is still using single-precision floats "
        "or the EPSILON/MAX_ITERATIONS values were not correctly extracted and applied."
    )

def test_pricing_service_missing_param():
    """Verify the pricing service handles missing parameters correctly."""
    url = "http://127.0.0.1:8080/price"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the pricing service at {url}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for missing parameter, got {response.status_code}"