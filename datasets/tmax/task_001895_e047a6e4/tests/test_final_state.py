# test_final_state.py
import pytest
import requests
import hashlib

BASE_URL = "http://127.0.0.1:8080"
SECRET = "OMEGA_PROTOCOL_7734"

def get_expected_token(username: str) -> str:
    data = f"{username}{SECRET}"
    sig = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return f"{username}:{sig}"

def test_service_running():
    """Verify the service is running and accepting connections."""
    try:
        # A simple GET or POST to check if port is open
        requests.get(BASE_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080 or refused connection.")
    except requests.exceptions.RequestException:
        pass # Other errors are fine, just checking if port is open

def test_generate_endpoint():
    """Verify the /generate endpoint returns the correct token format."""
    username = "alice"
    expected_token = get_expected_token(username)

    try:
        response = requests.post(f"{BASE_URL}/generate", json={"user": username}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /generate failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert "token" in data, "Response JSON missing 'token' key"
    assert data["token"] == expected_token, f"Expected token {expected_token}, got {data['token']}"

def test_validate_endpoint_valid():
    """Verify the /validate endpoint correctly validates a good token."""
    token = get_expected_token("alice")

    try:
        response = requests.post(f"{BASE_URL}/validate", json={"token": token}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /validate failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert "valid" in data, "Response JSON missing 'valid' key"
    assert data["valid"] is True, f"Expected valid=True, got {data['valid']}"

def test_validate_endpoint_invalid_hash():
    """Verify the /validate endpoint rejects a token with an incorrect hash."""
    token = "alice:wronghash12345"

    try:
        response = requests.post(f"{BASE_URL}/validate", json={"token": token}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /validate failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert "valid" in data, "Response JSON missing 'valid' key"
    assert data["valid"] is False, f"Expected valid=False, got {data['valid']}"

def test_validate_endpoint_invalid_user():
    """Verify the /validate endpoint rejects a token with a mismatched user."""
    # Using alice's hash for bob
    alice_token = get_expected_token("alice")
    alice_hash = alice_token.split(":")[1]
    token = f"bob:{alice_hash}"

    try:
        response = requests.post(f"{BASE_URL}/validate", json={"token": token}, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /validate failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert "valid" in data, "Response JSON missing 'valid' key"
    assert data["valid"] is False, f"Expected valid=False, got {data['valid']}"