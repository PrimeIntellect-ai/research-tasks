# test_final_state.py

import os
import requests
import pytest

API_URL = "http://127.0.0.1:9090"
AUTH_HEADER = {"Authorization": "Bearer DBRE-SEC-991"}

def test_api_pid_file():
    pid_file = "/home/user/api.pid"
    assert os.path.exists(pid_file), f"PID file not found at {pid_file}"
    with open(pid_file, "r") as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"PID file does not contain a valid integer: {pid}"

def test_auth_required():
    # Missing auth
    resp = requests.get(f"{API_URL}/critical_nodes")
    assert resp.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {resp.status_code}"

    # Bad auth
    bad_auth = {"Authorization": "Bearer BAD-TOKEN"}
    resp = requests.get(f"{API_URL}/critical_nodes", headers=bad_auth)
    assert resp.status_code in (401, 403), f"Expected 401 or 403 for bad auth, got {resp.status_code}"

def test_critical_nodes():
    # Test pagination and filtering
    params = {
        "limit": 2,
        "offset": 1,
        "min_centrality": 0.1
    }
    resp = requests.get(f"{API_URL}/critical_nodes", headers=AUTH_HEADER, params=params)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    data = resp.json()
    assert isinstance(data, list), "Expected a JSON array"
    assert len(data) == 2, f"Expected 2 items, got {len(data)}"

    # Expected nodes after sorting by centrality desc, then name asc:
    # 1. db-primary (0.4)
    # 2. db-analytics-1 (0.2)
    # 3. db-replica-1 (0.2)
    # 4. db-replica-2 (0.2)
    # Offset 1, limit 2 -> db-analytics-1, db-replica-1

    assert data[0]["node"] == "db-analytics-1", f"Expected db-analytics-1, got {data[0]['node']}"
    assert abs(data[0]["centrality"] - 0.2) < 1e-5, f"Expected centrality ~0.2, got {data[0]['centrality']}"

    assert data[1]["node"] == "db-replica-1", f"Expected db-replica-1, got {data[1]['node']}"
    assert abs(data[1]["centrality"] - 0.2) < 1e-5, f"Expected centrality ~0.2, got {data[1]['centrality']}"

def test_backup_chain():
    resp = requests.get(f"{API_URL}/backup_chain/db-primary", headers=AUTH_HEADER)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    data = resp.json()
    assert isinstance(data, list), "Expected a JSON array"

    expected_chain = ["db-analytics-1", "db-archive", "db-replica-1", "db-replica-2", "db-reporting"]
    assert data == expected_chain, f"Expected {expected_chain}, got {data}"