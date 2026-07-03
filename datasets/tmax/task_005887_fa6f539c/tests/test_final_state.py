# test_final_state.py
import pytest
import requests
import json
import hashlib
import os
import signal
import time

URL = "http://127.0.0.1:8000/api/v1/sync"
MASTER_FILE = "/home/user/state/master.json"
LOG_FILE = "/home/user/state/sync.log"
PID_FILE = "/home/user/server.pid"

def hash_ids(ids):
    return hashlib.sha256("".join(map(str, ids)).encode()).hexdigest()

def test_server_pid_exists():
    assert os.path.exists(PID_FILE), f"PID file {PID_FILE} not found. Server may not be running in the background."
    with open(PID_FILE, 'r') as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file {PID_FILE} does not contain a valid integer PID."

def test_server_logic_and_state():
    # Test 1: Valid request
    tx1 = [{"id": 105, "ts": 1690000005, "val": "A"}, {"id": 102, "ts": 1690000001, "val": "B"}]
    try:
        resp1 = requests.post(URL, json={
            "client_id": "client_A",
            "checksum": hash_ids([105, 102]),
            "transactions": tx1
        }, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {URL}: {e}")

    assert resp1.status_code == 200, f"Expected 200 for valid request, got {resp1.status_code}"

    # Test 2: Invalid checksum
    tx2 = [{"id": 108, "ts": 1690000010, "val": "C"}]
    resp2 = requests.post(URL, json={
        "client_id": "client_A",
        "checksum": "invalid_hash_value",
        "transactions": tx2
    }, timeout=2)
    assert resp2.status_code == 400, f"Expected 400 for invalid checksum, got {resp2.status_code}"

    # Test 3: Rate limiting
    tx3 = [{"id": 102, "ts": 1690000001, "val": "B_dup"}, {"id": 103, "ts": 1690000003, "val": "D"}]
    resp3 = requests.post(URL, json={
        "client_id": "client_A",
        "checksum": hash_ids([102, 103]),
        "transactions": tx3
    }, timeout=2)
    assert resp3.status_code == 429, f"Expected 429 for rate limit exceeded (3rd request), got {resp3.status_code}"

    # Test 4: Valid request on different client
    resp4 = requests.post(URL, json={
        "client_id": "client_B",
        "checksum": hash_ids([102, 103]),
        "transactions": tx3
    }, timeout=2)
    assert resp4.status_code == 200, f"Expected 200 for valid request on a new client, got {resp4.status_code}"

    # Verify State File
    assert os.path.exists(MASTER_FILE), f"Master state file {MASTER_FILE} not found."
    with open(MASTER_FILE, 'r') as f:
        try:
            master = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Master state file {MASTER_FILE} is not valid JSON.")

    expected_ids = [100, 102, 103, 105]
    actual_ids = [t.get('id') for t in master]
    assert actual_ids == expected_ids, f"Expected transaction IDs in order {expected_ids}, got {actual_ids}"

    # Verify Log File
    assert os.path.exists(LOG_FILE), f"Sync log file {LOG_FILE} not found."
    with open(LOG_FILE, 'r') as f:
        logs = f.read().strip().split('\n')

    logs = [log for log in logs if log]
    assert len(logs) == 2, f"Expected exactly 2 log lines, got {len(logs)}"
    assert logs[0] == "SYNC client_A: Added 2 transactions: 102, 105", f"First log line mismatch: {logs[0]}"
    assert logs[1] == "SYNC client_B: Added 1 transactions: 103", f"Second log line mismatch: {logs[1]}"

def test_teardown_server():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid_str = f.read().strip()
        if pid_str.isdigit():
            try:
                os.kill(int(pid_str), signal.SIGTERM)
            except ProcessLookupError:
                pass