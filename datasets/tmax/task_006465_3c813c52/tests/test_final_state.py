# test_final_state.py

import os
import json
import socket
import pytest
import glob

STATUS_FILE = "/home/user/operator_status.json"
MANIFESTS_DIR = "/home/user/manifests"

def get_actual_manifest_bytes():
    total_size = 0
    pattern = os.path.join(MANIFESTS_DIR, "*.yaml")
    for filepath in glob.glob(pattern):
        if os.path.isfile(filepath):
            total_size += os.path.getsize(filepath)
    return total_size

def is_api_reachable():
    host = "127.0.0.1"
    port = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((host, port))
        return result == 0

def test_operator_status_json_exists():
    assert os.path.isfile(STATUS_FILE), f"The file {STATUS_FILE} does not exist."

def test_operator_status_json_content():
    assert os.path.isfile(STATUS_FILE), f"The file {STATUS_FILE} does not exist."

    with open(STATUS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {STATUS_FILE} does not contain valid JSON.")

    assert "manifest_bytes" in data, "Key 'manifest_bytes' missing in JSON."
    assert "api_reachable" in data, "Key 'api_reachable' missing in JSON."
    assert "status" in data, "Key 'status' missing in JSON."

    expected_bytes = get_actual_manifest_bytes()
    expected_reachable = is_api_reachable()
    expected_status = "healthy" if expected_reachable and expected_bytes <= 1048576 else "unhealthy"

    assert data["manifest_bytes"] == expected_bytes, f"Expected manifest_bytes to be {expected_bytes}, but got {data['manifest_bytes']}."
    assert data["api_reachable"] == expected_reachable, f"Expected api_reachable to be {expected_reachable}, but got {data['api_reachable']}."
    assert data["status"] == expected_status, f"Expected status to be '{expected_status}', but got '{data['status']}'."