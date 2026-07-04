# test_final_state.py

import os
import json
import requests
import pytest

URL = "http://127.0.0.1:8080/ingest"
SECRET = "sk_live_9f8d7c6b5a4e3f2d1c0b"
HEADERS = {"Authorization": f"Bearer {SECRET}"}

def test_service_auth():
    """Test that the service rejects unauthorized requests and accepts authorized ones."""
    # Unauthorized
    try:
        resp = requests.post("http://127.0.0.1:8080/ingest", json={"test": "data"}, timeout=2)
        assert resp.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {resp.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running or not listening on 127.0.0.1:8080")

def test_precision_fix():
    """Test that the service maintains Decimal precision for *_coord keys."""
    payload = {"x_coord": "123.4567890123456789", "data": "valid"}
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"

    data = resp.json()
    # The server should echo back the decoded data or similar, preserving the exact string
    # We check if the exact high-precision string is in the response text
    assert "123.4567890123456789" in resp.text, "High-precision decimal value was lost in the response."

def test_corrupted_utf8():
    """Test that corrupted UTF-8 payloads do not crash the server."""
    bad_payload = b'{"data": "invalid \xff\xff"}'
    headers = HEADERS.copy()
    headers["Content-Type"] = "application/json"

    resp = requests.post(URL, headers=headers, data=bad_payload, timeout=2)
    # Should not be 500 Internal Server Error
    assert resp.status_code != 500, "Server crashed (500) on invalid UTF-8 payload."

def test_decoder_code_fixes():
    """Test that the decoder.py file was actually modified to fix the issues."""
    decoder_path = "/app/vendored/telemetry-decoder/decoder.py"
    assert os.path.isfile(decoder_path), "decoder.py is missing."

    with open(decoder_path, "r") as f:
        content = f.read()

    assert "Decimal" in content, "decoder.py does not use Decimal for precision."
    assert "float(" not in content or "float" not in content.split("Decimal")[1], "decoder.py still seems to use float() for coordinates."