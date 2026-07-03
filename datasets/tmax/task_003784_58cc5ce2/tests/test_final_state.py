# test_final_state.py

import os
import stat
import json
import base64
import pytest
import requests

def decode_base64url(data):
    """Helper to decode base64url with missing padding."""
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding).decode('utf-8')

def test_admin_exploit_jwt_file():
    """Test that the admin_exploit.jwt file exists, has correct permissions, and contains a valid alg:none payload."""
    jwt_path = '/home/user/admin_exploit.jwt'
    assert os.path.exists(jwt_path), f"Exploit file not found at {jwt_path}"

    # Check permissions (strictly 0600)
    st = os.stat(jwt_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions for {jwt_path} must be 0600, found {oct(perms)}"

    # Check JWT contents
    with open(jwt_path, 'r') as f:
        jwt_content = f.read().strip()

    parts = jwt_content.split('.')
    assert len(parts) in [2, 3], "JWT must have at least a header and payload separated by dots"

    try:
        header = json.loads(decode_base64url(parts[0]))
        payload = json.loads(decode_base64url(parts[1]))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT header/payload: {e}")

    assert header.get('alg', '').lower() == 'none', "JWT header must specify 'alg': 'none'"
    assert payload.get('user') == 'admin', "JWT payload must specify 'user': 'admin'"

def test_proxy_blocks_insecure_jwt():
    """Test that the proxy rejects alg:none JWTs with a 403 Forbidden."""
    # Construct an alg:none JWT
    header = base64.urlsafe_b64encode(b'{"alg":"none"}').decode('utf-8').rstrip('=')
    payload = base64.urlsafe_b64encode(b'{"user":"test"}').decode('utf-8').rstrip('=')
    jwt = f"{header}.{payload}."

    try:
        response = requests.get(
            'http://127.0.0.1:8080/profile',
            headers={'Authorization': f'Bearer {jwt}'},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at 127.0.0.1:8080: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 for alg:none JWT, got {response.status_code}"

def test_proxy_allows_valid_jwt_and_redacts_ssn():
    """Test that the proxy forwards valid JWTs and redacts the SSN in the response."""
    # Construct a dummy HS256 JWT (the legacy service accepts it if alg != none)
    header = base64.urlsafe_b64encode(b'{"alg":"HS256"}').decode('utf-8').rstrip('=')
    payload = base64.urlsafe_b64encode(b'{"user":"test"}').decode('utf-8').rstrip('=')
    signature = "dummysignature"
    jwt = f"{header}.{payload}.{signature}"

    try:
        response = requests.get(
            'http://127.0.0.1:8080/profile',
            headers={'Authorization': f'Bearer {jwt}'},
            timeout=2
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid JWT, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("Response from proxy was not valid JSON")

    assert 'ssn' in data, "Response JSON did not contain 'ssn' key"
    assert data['ssn'] == '***-**-****', f"SSN was not properly redacted. Got: {data['ssn']}"

def test_security_audit_log():
    """Test that the security audit log exists, has correct permissions, and contains the rejection log."""
    log_path = '/home/user/security_audit.log'
    assert os.path.exists(log_path), f"Audit log not found at {log_path}"

    # Check permissions (strictly 0600)
    st = os.stat(log_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions for {log_path} must be 0600, found {oct(perms)}"

    # Check log contents
    with open(log_path, 'r') as f:
        log_content = f.read()

    expected_log = "[REJECTED] IP:127.0.0.1 REASON:Insecure_JWT"
    assert expected_log in log_content, f"Audit log does not contain the expected rejection string: '{expected_log}'"