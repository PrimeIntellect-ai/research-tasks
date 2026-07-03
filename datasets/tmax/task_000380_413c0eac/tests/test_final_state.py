# test_final_state.py

import json
import math
import requests
import pytest

SERVER_URL = "http://127.0.0.1:8080/variance"

def test_variance_catastrophic_cancellation():
    """
    Test that the server calculates the correct variance for a dataset that
    would cause catastrophic cancellation in the naive algorithm.
    """
    payload = {"data": [100000000.1, 100000000.2, 100000000.3]}
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {SERVER_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Server did not return valid JSON. Response: {response.text}")

    assert "variance" in data, f"Response JSON missing 'variance' key. Got: {data}"

    variance = data["variance"]
    expected_variance = 0.01

    assert math.isclose(variance, expected_variance, rel_tol=1e-5), \
        f"Variance calculation is incorrect. Expected ~{expected_variance}, got {variance}."

def test_variance_precision_serialization():
    """
    Test that the server serializes floating-point numbers with high precision
    and does not truncate to 2 decimal places.
    """
    payload = {"data": [1.0, 2.0, 4.0]}
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {SERVER_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    # Check the raw text to ensure it has more than 2 decimal places
    raw_text = response.text
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        pytest.fail(f"Server did not return valid JSON. Response: {raw_text}")

    assert "variance" in data, f"Response JSON missing 'variance' key. Got: {data}"

    variance_str = str(data["variance"])
    # The exact variance is 7/3 = 2.3333333333333335
    # If the precision is truncated to 2 decimal places, it will be "2.33"

    # We check if the string representation in the raw JSON has more than 4 characters for the fractional part
    # Or we can just check if the parsed float is close to 2.3333333333333335 and strictly not equal to 2.33
    variance = data["variance"]
    expected_variance = 7.0 / 3.0

    assert math.isclose(variance, expected_variance, rel_tol=1e-5), \
        f"Variance calculation is incorrect. Expected ~{expected_variance}, got {variance}."

    assert variance != 2.33, \
        f"Variance precision appears to be truncated to 2 decimal places. Raw response: {raw_text}"