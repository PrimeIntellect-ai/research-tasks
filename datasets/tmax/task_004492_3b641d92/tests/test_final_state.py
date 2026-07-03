# test_final_state.py
import os
import requests
import pytest
import time

PORT = 9095
BASE_URL = f"http://127.0.0.1:{PORT}"
CONFIGS_DIR = "/home/user/configs"
EXPECTED_TOKEN = "X9F2B-88ZZ1"

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_files_extracted_and_renamed():
    assert os.path.isdir(CONFIGS_DIR), f"Directory {CONFIGS_DIR} does not exist."

    router_file = os.path.join(CONFIGS_DIR, "router_A.json")
    switch_file = os.path.join(CONFIGS_DIR, "switch_B.json")

    assert os.path.isfile(router_file), f"File {router_file} does not exist."
    assert os.path.isfile(switch_file), f"File {switch_file} does not exist."

    with open(router_file, "r") as f:
        content = f.read()
        assert EXPECTED_TOKEN in content, f"Token placeholder not replaced in {router_file}."
        assert "{{TOKEN_PLACEHOLDER}}" not in content, f"Token placeholder still exists in {router_file}."

def test_server_router_a():
    assert wait_for_server(f"{BASE_URL}/api/config/router_A.json"), "Server is not reachable on port 9095."

    response = requests.get(f"{BASE_URL}/api/config/router_A.json")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}."
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type application/json."

    data = response.json()
    assert data.get("device") == "router_A", f"Expected device router_A, got {data.get('device')}."
    assert data.get("auth") == EXPECTED_TOKEN, f"Expected auth {EXPECTED_TOKEN}, got {data.get('auth')}."

def test_server_switch_b():
    assert wait_for_server(f"{BASE_URL}/api/config/switch_B.json"), "Server is not reachable on port 9095."

    response = requests.get(f"{BASE_URL}/api/config/switch_B.json")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}."
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type application/json."

    data = response.json()
    assert data.get("device") == "switch_B", f"Expected device switch_B, got {data.get('device')}."
    assert data.get("auth") == EXPECTED_TOKEN, f"Expected auth {EXPECTED_TOKEN}, got {data.get('auth')}."

def test_server_corrupted():
    assert wait_for_server(f"{BASE_URL}/api/config/router_A.json"), "Server is not reachable on port 9095."

    response = requests.get(f"{BASE_URL}/api/config/corrupted.json")
    assert response.status_code == 404, f"Expected status 404 for corrupted.json, got {response.status_code}."