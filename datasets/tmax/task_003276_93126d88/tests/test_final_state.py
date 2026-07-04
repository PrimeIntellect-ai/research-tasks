# test_final_state.py

import os
import json
import struct
import math
import requests
import pytest
import hashlib
import unicodedata

def pack_record(t, val, user, text):
    """Pack a record into the custom binary format."""
    b_t = struct.pack('<I', t)
    b_val = struct.pack('<f', val) if val is not None else struct.pack('<f', float('nan'))
    b_user = user.encode('utf-8').ljust(16, b'\x00')[:16]
    b_text = text.encode('utf-8') + b'\x00'
    return b_t + b_val + b_user + b_text

def test_server_processing():
    """Test the HTTP server's processing logic."""
    url = "http://127.0.0.1:9090/process"
    headers = {"Authorization": "Bearer secr3t_t0k3n"}

    # Construct binary payload
    payload = b""
    payload += pack_record(100, 5.5, "alice", "Mo\u0308tley") # NFD
    payload += pack_record(100, 5.5, "alice", "Mo\u0308tley") # Duplicate
    payload += pack_record(102, None, "bob", "CAF\u00c9")     # NFC

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    lines = response.text.strip().split('\n')
    assert len(lines) == 3, f"Expected 3 lines of JSON, got {len(lines)}"

    records = []
    for i, line in enumerate(lines):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON on line {i+1}: {line}")

    # Expected values
    # Record 1
    assert records[0]["timestamp"] == 100
    assert records[0]["text_note"] == "mötley"
    assert records[0]["sensor_val"] == 5.5
    assert records[0]["user_id"] == hashlib.sha256(b"alice").hexdigest()

    # Record 2 (Filled)
    assert records[1]["timestamp"] == 101
    assert records[1]["text_note"] == ""
    assert records[1]["sensor_val"] == 5.5
    assert records[1]["user_id"] == hashlib.sha256(b"SYSTEM").hexdigest()

    # Record 3
    assert records[2]["timestamp"] == 102
    assert records[2]["text_note"] == "café"
    assert records[2]["sensor_val"] == 5.5
    assert records[2]["user_id"] == hashlib.sha256(b"bob").hexdigest()

def test_server_unauthorized():
    """Test the HTTP server rejects unauthorized requests."""
    url = "http://127.0.0.1:9090/process"
    headers = {"Authorization": "Bearer wrong_token"}
    payload = pack_record(100, 5.5, "alice", "test")

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code in [401, 403], f"Expected HTTP 401 or 403 for unauthorized request, got {response.status_code}"

def test_server_log_exists():
    """Test that the server log exists and has content."""
    log_path = "/home/user/server.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        content = f.read()
    assert len(content.strip()) > 0, f"Log file {log_path} is empty."