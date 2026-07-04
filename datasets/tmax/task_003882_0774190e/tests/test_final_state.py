# test_final_state.py

import pytest
import requests

SERVER_URL = "http://127.0.0.1:8080/api/v1/translations"
AUTH_HEADER = {"Authorization": "Bearer loc-agent-2024"}

def test_server_running_and_unauthorized_without_header():
    """Test that the server is running and requires authorization."""
    try:
        response = requests.get(SERVER_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running on 127.0.0.1:8080 or refused the connection.")

    assert response.status_code == 401, f"Expected 401 Unauthorized when no Authorization header is provided, got {response.status_code}."

def test_server_unauthorized_with_bad_header():
    """Test that the server rejects invalid authorization headers."""
    bad_headers = {"Authorization": "Bearer invalid-token"}
    response = requests.get(SERVER_URL, headers=bad_headers, timeout=5)
    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}."

def test_server_returns_correct_json_with_valid_auth():
    """Test that the server returns the correctly filtered and decoded translations."""
    response = requests.get(SERVER_URL, headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {response.text}")

    assert "translations" in data, "JSON response must contain a 'translations' key."

    translations = data["translations"]
    assert isinstance(translations, dict), "'translations' must be a JSON object."

    expected_translations = {
        "msg_welcome": "Welcome back, {user}!",
        "msg_french": "Bonjour {user}, le café coûte 5€."
    }

    assert translations == expected_translations, f"Expected translations {expected_translations}, but got {translations}. Check decoding and filtering logic."