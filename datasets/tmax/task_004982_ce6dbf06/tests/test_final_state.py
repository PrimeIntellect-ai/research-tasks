# test_final_state.py

import os
import urllib.request
import urllib.error
import socket
import pytest

def test_secure_proxy_exists():
    """Verify that the secure proxy script has been created."""
    proxy_path = "/home/user/secure_proxy.py"
    assert os.path.isfile(proxy_path), f"Expected proxy script {proxy_path} does not exist."

def test_audit_report_contents():
    """Verify that the audit report exists and contains the correct extracted and tested values."""
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, f"Audit report should contain at least 3 lines, found {len(lines)}."

    expected_lines = {
        "LEGACY_TOKEN=OLD_COMPROMISED_KEY_9921",
        "PROXY_VALID=200",
        "PROXY_INVALID=403"
    }

    actual_lines = set(lines)
    missing = expected_lines - actual_lines
    assert not missing, f"Audit report is missing expected lines: {missing}. Found: {actual_lines}"

def test_proxy_port_listening():
    """Verify that the proxy is listening on port 9090."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "Proxy is not listening on 127.0.0.1:9090."

def test_legacy_worker_port_listening():
    """Verify that the legacy worker is listening on port 8080."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Legacy worker is not listening on 127.0.0.1:8080."

def test_proxy_enforces_rotated_token():
    """Verify that the proxy correctly accepts the new token and proxies the request."""
    req = urllib.request.Request("http://127.0.0.1:9090/")
    req.add_header("Authorization", "Bearer ROTATED_TOKEN_2024")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
            body = response.read().decode('utf-8')
            assert "Success!" in body, "Proxy did not return the expected success message from the legacy worker."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Proxy rejected valid rotated token with HTTP {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy: {e.reason}")

def test_proxy_rejects_invalid_token():
    """Verify that the proxy rejects invalid tokens with a 403 Forbidden."""
    req = urllib.request.Request("http://127.0.0.1:9090/")
    req.add_header("Authorization", "Bearer INVALID_TOKEN_123")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail(f"Proxy accepted invalid token and returned HTTP {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 Forbidden for invalid token, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy: {e.reason}")

def test_proxy_rejects_missing_token():
    """Verify that the proxy rejects requests missing the Authorization header."""
    req = urllib.request.Request("http://127.0.0.1:9090/")

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail(f"Proxy accepted request with missing token and returned HTTP {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 Forbidden for missing token, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy: {e.reason}")