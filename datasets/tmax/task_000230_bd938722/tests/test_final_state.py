# test_final_state.py

import os
import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
TOKEN = "SECRET-ETL-774"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

PAYLOAD = """{"tx_id": "cfg_db_host", "timestamp": 100, "config_value": "db1.local"}
{"tx_id": "cfg_db_port", "timestamp": 105, "config_value": "5432"}
{"tx_id": "cfg_db_host", "timestamp": 90, "config_value": "old.db.local"}
{"tx_id": "cfg_db_port", "timestamp": 110, "config_value": "5433"}"""

def test_ingest_unauthorized():
    """Test that POST /ingest without token or with bad token returns 401."""
    try:
        resp1 = requests.post(f"{BASE_URL}/ingest", data=PAYLOAD)
        assert resp1.status_code == 401, f"Expected 401 without auth, got {resp1.status_code}"

        resp2 = requests.post(f"{BASE_URL}/ingest", headers={"Authorization": "Bearer BAD-TOKEN"}, data=PAYLOAD)
        assert resp2.status_code == 401, f"Expected 401 with bad auth, got {resp2.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server. Is it running on 127.0.0.1:8080?")

def test_ingest_and_state():
    """Test POST /ingest with correct auth and GET /state."""
    try:
        # Clear the state if possible, though we assume a fresh server or that it processes this specific payload
        # Send payload
        resp_post = requests.post(f"{BASE_URL}/ingest", headers=HEADERS, data=PAYLOAD)
        assert resp_post.status_code == 200, f"Expected 200 OK for ingest, got {resp_post.status_code}"

        # Get state
        resp_get = requests.get(f"{BASE_URL}/state")
        assert resp_get.status_code == 200, f"Expected 200 OK for state, got {resp_get.status_code}"

        state_data = resp_get.json()
        expected_state = {
            "cfg_db_host": "db1.local",
            "cfg_db_port": "5433"
        }

        assert state_data.get("cfg_db_host") == "db1.local", f"Expected cfg_db_host to be 'db1.local', got {state_data.get('cfg_db_host')}"
        assert state_data.get("cfg_db_port") == "5433", f"Expected cfg_db_port to be '5433', got {state_data.get('cfg_db_port')}"

    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server. Is it running on 127.0.0.1:8080?")

def test_dropped_log():
    """Test that the dropped record was logged correctly."""
    log_path = "/home/user/dropped.log"
    assert os.path.exists(log_path), f"Dropped log file not found at {log_path}"

    with open(log_path, "r") as f:
        lines = f.read().strip().split("\n")

    # We expect at least one dropped record matching the one we sent
    found = False
    for line in lines:
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            if record.get("tx_id") == "cfg_db_host" and record.get("timestamp") == 90 and record.get("config_value") == "old.db.local":
                found = True
                break
        except json.JSONDecodeError:
            pass

    assert found, f"Expected dropped record not found in {log_path}. File contents: {lines}"