# test_final_state.py
import os
import sys
import pytest
import requests
import time

def test_libdag_installed():
    try:
        import libdag
        assert hasattr(libdag, 'topological_sort'), "libdag installed but missing topological_sort"
    except ImportError:
        pytest.fail("libdag is not installed in the system environment.")

def test_service_endpoints_and_rate_limit():
    base_url = "http://127.0.0.1:8080"
    headers = {
        "Authorization": "Bearer ci-deploy-token-8842",
        "Content-Type": "application/json"
    }

    # 1. Test /resolve
    resolve_payload = {
        "graph": {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    }
    try:
        resp_resolve = requests.post(f"{base_url}/resolve", json=resolve_payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service at {base_url}/resolve: {e}")

    assert resp_resolve.status_code == 200, f"Expected 200 for /resolve, got {resp_resolve.status_code}. Response: {resp_resolve.text}"
    data = resp_resolve.json()
    assert "build_order" in data, "Missing 'build_order' in response"
    valid_orders = [["D", "B", "C", "A"], ["D", "C", "B", "A"]]
    assert data["build_order"] in valid_orders, f"Incorrect build order: {data['build_order']}"

    # 2. Test /filter_versions
    filter_payload = {
        "versions": ["0.9.9", "1.2.4", "1.9.0", "2.0.1"],
        "constraint": ">=1.0.0 <2.0.0"
    }
    resp_filter = requests.post(f"{base_url}/filter_versions", json=filter_payload, headers=headers, timeout=5)
    assert resp_filter.status_code == 200, f"Expected 200 for /filter_versions, got {resp_filter.status_code}. Response: {resp_filter.text}"
    data_filter = resp_filter.json()
    assert "compliant" in data_filter, "Missing 'compliant' in response"
    assert sorted(data_filter["compliant"]) == ["1.2.4", "1.9.0"], f"Incorrect compliant versions: {data_filter['compliant']}"

    # 3. Test Rate Limiting
    # We have made 2 requests so far. We need to make 4 more.
    # Requests 3, 4, 5 should be 200. Request 6 should be 429.
    for i in range(3, 6):
        resp = requests.post(f"{base_url}/filter_versions", json=filter_payload, headers=headers, timeout=5)
        assert resp.status_code == 200, f"Expected request {i} to be 200, got {resp.status_code}"

    # Request 6
    resp_429 = requests.post(f"{base_url}/filter_versions", json=filter_payload, headers=headers, timeout=5)
    assert resp_429.status_code == 429, f"Expected request 6 to be 429, got {resp_429.status_code}"

def test_log_file_exists():
    log_path = "/home/user/service.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, "Log file is empty."