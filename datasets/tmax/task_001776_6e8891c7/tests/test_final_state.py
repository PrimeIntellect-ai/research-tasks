# test_final_state.py
import math
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080/generate"
AUTH_HEADER = {"Authorization": "Bearer ML-DATA-TOKEN"}

def test_missing_auth():
    payload = {"a": 10.0, "mu": 50.0, "sigma": 5.0, "noise_level": 0.0, "baseline_slope": 0.1}
    try:
        resp = requests.post(BASE_URL, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API on 127.0.0.1:8080. Is the server running?")

    assert resp.status_code == 401, f"Expected 401 Unauthorized when missing auth, got {resp.status_code}. Body: {resp.text}"

def test_invalid_auth():
    payload = {"a": 10.0, "mu": 50.0, "sigma": 5.0, "noise_level": 0.0, "baseline_slope": 0.1}
    headers = {"Authorization": "Bearer INVALID-TOKEN"}
    resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=5)

    assert resp.status_code == 401, f"Expected 401 Unauthorized with invalid auth, got {resp.status_code}. Body: {resp.text}"

def test_successful_generation_and_augmentation():
    payload = {"a": 10.0, "mu": 50.0, "sigma": 5.0, "noise_level": 0.0, "baseline_slope": 0.1}
    resp = requests.post(BASE_URL, json=payload, headers=AUTH_HEADER, timeout=5)

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {resp.text}")

    assert "spectrum" in data, "Response JSON missing 'spectrum' key."
    assert "fitted_mu" in data, "Response JSON missing 'fitted_mu' key."

    spectrum = data["spectrum"]
    assert isinstance(spectrum, list), "'spectrum' should be a list."
    assert len(spectrum) == 100, f"Expected 100 points in spectrum, got {len(spectrum)}."

    # Calculate the expected spectrum (binary output + baseline drift)
    # Since noise_level is 0.0, it should match exactly.
    for i in range(100):
        base_val = 10.0 * math.exp(-((i - 50.0)**2) / (2 * 5.0**2))
        expected_val = base_val + (i * 0.1)

        # Allow a small tolerance for floating point and formatting differences from the C++ binary
        assert abs(spectrum[i] - expected_val) < 1e-4, \
            f"Spectrum mismatch at index {i}. Expected ~{expected_val}, got {spectrum[i]}."

    fitted_mu = data["fitted_mu"]
    assert isinstance(fitted_mu, float) or isinstance(fitted_mu, int), "'fitted_mu' should be a number."
    assert abs(fitted_mu - 50.0) < 1e-2, f"Expected fitted_mu to be very close to 50.0, got {fitted_mu}."

def test_validation_failure_due_to_high_noise():
    # Massive noise to guarantee curve fitting fails or gives a completely wrong mu
    payload = {"a": 1.0, "mu": 50.0, "sigma": 5.0, "noise_level": 10000.0, "baseline_slope": 0.1}
    resp = requests.post(BASE_URL, json=payload, headers=AUTH_HEADER, timeout=5)

    assert resp.status_code == 400, f"Expected 400 Bad Request for validation failure, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {resp.text}")

    assert data.get("error") == "Validation failed", f"Expected error message 'Validation failed', got: {data.get('error')}"