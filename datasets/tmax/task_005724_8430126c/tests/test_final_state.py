# test_final_state.py

import os
import re
import ssl
import urllib.request
import urllib.error
import pytest

def get_backdoor_token():
    binary_path = "/home/user/legacy_api"
    if not os.path.exists(binary_path):
        return None
    with open(binary_path, "rb") as f:
        content = f.read()

    match = re.search(b"BACKDOOR_TOKEN=([A-Za-z0-9_!@#$%^&*]+)", content)
    if match:
        return match.group(1).decode('utf-8')
    return None

def test_tls_certificates_exist():
    crt_path = "/home/user/server.crt"
    key_path = "/home/user/server.key"
    assert os.path.isfile(crt_path), f"TLS certificate not found at {crt_path}"
    assert os.path.isfile(key_path), f"TLS private key not found at {key_path}"

def test_proxy_normal_traffic():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request("https://127.0.0.1:8443/normal_test")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy or proxy returned error: {e}")

def test_proxy_blocks_backdoor_token():
    token = get_backdoor_token()
    assert token is not None, "Could not extract BACKDOOR_TOKEN from legacy_api binary."

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request("https://127.0.0.1:8443/secret_test")
    req.add_header("Cookie", f"admin_token={token}")

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
            pytest.fail(f"Expected HTTP 403 Forbidden, but request succeeded with status {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 Forbidden, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy: {e}")

def test_proxy_redacts_sensitive_data():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    auth_val = "Bearer supersecret12345"
    session_val = "session98765"

    req = urllib.request.Request("https://127.0.0.1:8443/data_test")
    req.add_header("Authorization", auth_val)
    req.add_header("Cookie", f"session_id={session_val}")

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy or proxy returned error: {e}")

    log_path = "/home/user/proxy.log"
    assert os.path.isfile(log_path), f"Proxy log not found at {log_path}"

    with open(log_path, "r") as f:
        logs = f.read()

    assert auth_val not in logs, "Sensitive Authorization header was not redacted in proxy.log"
    assert session_val not in logs, "Sensitive session_id cookie was not redacted in proxy.log"

    # Check for the specific log format requirements
    expected_redacted_log = "GET /data_test | Auth: [REDACTED] | Session: [REDACTED]"
    assert expected_redacted_log in logs, f"Expected log entry '{expected_redacted_log}' not found in proxy.log"

    expected_normal_log = "GET /normal_test | Auth: NONE | Session: NONE"
    assert expected_normal_log in logs, f"Expected log entry '{expected_normal_log}' not found in proxy.log"