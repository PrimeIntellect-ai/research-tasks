# test_final_state.py

import os
import socket
import pytest
import requests

def test_cracked_pin_file():
    pin_path = "/app/cracked_pin.txt"
    assert os.path.exists(pin_path), f"Cracked PIN file not found at {pin_path}"
    assert os.path.isfile(pin_path), f"{pin_path} is not a file"

    with open(pin_path, "r") as f:
        pin = f.read().strip()

    assert pin == "1234", f"Expected cracked PIN to be '1234', but got '{pin}'"

def test_audit_logger_running():
    """Verify that the audit_logger is listening on TCP port 9000."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 9000))
        assert result == 0, "audit_logger is not listening on 127.0.0.1:9000"

def test_evidence_api_normal_request():
    """Verify that the evidence_api HTTP service is running and handles valid requests."""
    try:
        resp = requests.get("http://127.0.0.1:8000/record?id=1", timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK for valid ID, got {resp.status_code}"
        assert resp.text.strip(), "Expected non-empty response for valid ID"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to evidence_api on port 8000: {e}")

def test_evidence_api_sqli_patched():
    """Verify that the SQL injection vulnerability has been patched."""
    try:
        # First, get the normal response to compare
        resp_normal = requests.get("http://127.0.0.1:8000/record?id=1", timeout=2)
        assert resp_normal.status_code == 200, "Normal request failed"

        # Test SQL injection payloads
        payloads = ["1' OR '1'='1", "1' OR 1=1--"]
        for payload in payloads:
            resp = requests.get(f"http://127.0.0.1:8000/record?id={payload}", timeout=2)

            # If the application still returns 200 OK, it should NOT return the same data as id=1
            # or all records. It should ideally be empty or a 404.
            if resp.status_code == 200:
                assert resp.text != resp_normal.text, f"SQL injection vulnerability still present with payload {payload}"
                # If it's a JSON array, it should be empty
                if resp.text.strip().startswith("["):
                    assert resp.text.strip() == "[]", f"SQL injection returned data: {resp.text}"
                else:
                    # If it's an object or string, ensure it doesn't look like valid record data
                    assert len(resp.text.strip()) < len(resp_normal.text.strip()), "SQL injection returned unexpected data length"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to evidence_api on port 8000 during SQLi test: {e}")