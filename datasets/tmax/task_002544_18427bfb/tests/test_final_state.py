# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/correlation"
EXPECTED_TOKEN = "ETL_SECURE_TOKEN_99X"
EXPECTED_CORRELATION = 0.9912

def test_no_auth():
    """Test that the endpoint returns 401 when no Authorization header is provided."""
    try:
        response = requests.get(BASE_URL, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server. Is it running on 127.0.0.1:8000?")

def test_invalid_auth():
    """Test that the endpoint returns 401 when an invalid Authorization header is provided."""
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server. Is it running on 127.0.0.1:8000?")

def test_valid_auth_and_response():
    """Test that the endpoint returns 200 and the correct correlation value when the correct token is provided."""
    headers = {"Authorization": f"Bearer {EXPECTED_TOKEN}"}
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail("Response is not valid JSON")

        assert "correlation" in data, "Response JSON is missing 'correlation' key"

        # Check if correlation is roughly equal to 0.9912 (allow float or string)
        actual_corr = float(data["correlation"])
        assert abs(actual_corr - EXPECTED_CORRELATION) < 1e-4, f"Expected correlation {EXPECTED_CORRELATION}, got {actual_corr}"

    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server. Is it running on 127.0.0.1:8000?")