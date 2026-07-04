# test_final_state.py
import pytest
import requests
import urllib3

# Suppress insecure request warnings since we are testing a self-signed cert on localhost
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECRET = "s3cr3t_f0r_m4lw4r3_9912"
EXPECTED_PAYLOAD = {"status": "ok", "payload": "EXEC_SHELL_9921"}
C2_URL = "https://127.0.0.1:8443/beacon"

def get_jwt_module():
    try:
        import jwt
        return jwt
    except ImportError:
        pytest.fail("The 'jwt' module is not installed. Did you install the repaired package from /app/vendored/pyjwt-2.8.0?")

def test_pyjwt_is_fixed():
    """Verify that the deliberate bug in pyjwt has been fixed."""
    jwt = get_jwt_module()
    payload = {"test": "data"}

    # Encode a token using the library
    token = jwt.encode(payload, SECRET, algorithm="HS256")

    try:
        # Attempt to decode it. If the sabotage is still there, this will raise an InvalidSignatureError.
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        assert decoded == payload, "Decoded payload does not match original."
    except Exception as e:
        pytest.fail(f"Failed to decode a valid JWT. The vendored pyjwt library is likely still sabotaged. Error: {e}")

def test_c2_server_valid_token():
    """Verify the C2 server responds correctly to a valid JWT."""
    jwt = get_jwt_module()
    token = jwt.encode({"role": "implant"}, SECRET, algorithm="HS256")

    # jwt.encode returns a string in newer pyjwt versions, but bytes in older ones. Ensure it's a string.
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(C2_URL, headers=headers, verify=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to C2 server at {C2_URL}. Ensure the server is running and listening on 127.0.0.1:8443.")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid token, got {response.status_code}. Response: {response.text}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert json_data == EXPECTED_PAYLOAD, f"Expected payload {EXPECTED_PAYLOAD}, got {json_data}"

def test_c2_server_invalid_token():
    """Verify the C2 server rejects an invalid JWT."""
    jwt = get_jwt_module()
    # Sign with the wrong secret
    token = jwt.encode({"role": "implant"}, "wrong_secret_123", algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode('utf-8')

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(C2_URL, headers=headers, verify=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to C2 server at {C2_URL}. Ensure the server is running.")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for invalid token, got {response.status_code}. Response: {response.text}"

def test_c2_server_missing_token():
    """Verify the C2 server rejects requests with no token."""
    try:
        response = requests.get(C2_URL, verify=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to C2 server at {C2_URL}. Ensure the server is running.")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {response.status_code}. Response: {response.text}"