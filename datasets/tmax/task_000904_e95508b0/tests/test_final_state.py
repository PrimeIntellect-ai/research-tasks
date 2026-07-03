# test_final_state.py

import os
import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

@pytest.fixture(scope="module")
def auth_token():
    token_path = "/app/config/auth_token.txt"
    assert os.path.isfile(token_path), f"Auth token file missing: {token_path}"
    with open(token_path, "r") as f:
        return f.read().strip()

@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

def test_setup_py_fixed():
    setup_path = "/app/backup_graph_lib-1.0.0/setup.py"
    assert os.path.isfile(setup_path), f"File missing: {setup_path}"
    with open(setup_path, "r") as f:
        content = f.read()
    assert "networkkxx" not in content, "The deliberate perturbation 'networkkxx' is still in setup.py"
    assert "networkx" in content, "The dependency 'networkx' is missing in setup.py"

def test_health_endpoint():
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_auth_required():
    try:
        resp = requests.get(f"{BASE_URL}/critical_nodes", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /critical_nodes: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized without auth, got {resp.status_code}"

def test_critical_nodes(auth_headers):
    try:
        resp = requests.get(f"{BASE_URL}/critical_nodes", headers=auth_headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /critical_nodes: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert "critical_nodes" in data, f"Missing 'critical_nodes' in response: {data}"

    nodes = data["critical_nodes"]
    assert len(nodes) == 3, f"Expected exactly 3 nodes, got {len(nodes)}"

    # b1 has in-degree 2, b4 has in-degree 1, others have 0
    assert nodes[0] == "b1", f"Expected 'b1' as most critical, got {nodes[0]}"
    assert nodes[1] == "b4", f"Expected 'b4' as second most critical, got {nodes[1]}"
    assert nodes[2] in ["b2", "b3", "b5"], f"Expected 3rd node to be one of b2, b3, b5, got {nodes[2]}"

def test_window_top_backups(auth_headers):
    try:
        resp = requests.get(f"{BASE_URL}/window_top_backups", headers=auth_headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /window_top_backups: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert "top_backups" in data, f"Missing 'top_backups' in response: {data}"

    top = data["top_backups"]
    assert "us-east" in top, "Missing 'us-east' in top_backups"
    assert "us-west" in top, "Missing 'us-west' in top_backups"

    assert top["us-east"] == ["b2", "b1"], f"Expected ['b2', 'b1'] for us-east, got {top['us-east']}"
    assert top["us-west"] == ["b5", "b4"], f"Expected ['b5', 'b4'] for us-west, got {top['us-west']}"

def test_aggregate(auth_headers):
    payload = {"match": {"region": "us-west"}, "sum": "size_mb"}
    try:
        resp = requests.post(f"{BASE_URL}/aggregate", json=payload, headers=auth_headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /aggregate: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert "result" in data, f"Missing 'result' in response: {data}"
    assert data["result"] == 500, f"Expected sum 500 for us-west, got {data['result']}"

    payload2 = {"match": {"region": "us-east"}, "sum": "size_mb"}
    try:
        resp2 = requests.post(f"{BASE_URL}/aggregate", json=payload2, headers=auth_headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /aggregate: {e}")

    assert resp2.status_code == 200, f"Expected 200 OK, got {resp2.status_code}"
    data2 = resp2.json()
    assert data2["result"] == 300, f"Expected sum 300 for us-east, got {data2['result']}"