# test_final_state.py
import os
import math
import subprocess
import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_service():
    """Wait for the service to be up and running."""
    for _ in range(10):
        try:
            # Just test if the port is open by sending a dummy GET to /top?n=1
            requests.get(f"{BASE_URL}/top?n=1", timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_service_is_up():
    assert wait_for_service(), f"Service at {BASE_URL} is not responding."

def test_setup_script_exists_and_executable():
    script_path = "/home/user/setup_and_run.sh"
    assert os.path.exists(script_path), f"Deployment script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

def test_analyze_endpoint():
    payload = {
        "files": [
            "/app/file_high_entropy.bin",
            "/app/file_low_entropy.txt",
            "/app/file_tiny.txt",
            "/app/non_existent_file.xyz"
        ]
    }
    resp = requests.post(f"{BASE_URL}/analyze", json=payload)
    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response: {resp.text}"

    data = resp.json()
    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("processed") == 3, f"Expected 3 valid files processed, got {data.get('processed')}"

def test_top_endpoint_ranking():
    # Fetch top 2
    resp = requests.get(f"{BASE_URL}/top?n=2")
    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response: {resp.text}"

    data = resp.json()
    assert isinstance(data, list), "Expected a JSON list from /top"
    assert len(data) == 2, f"Expected 2 items, got {len(data)}"

    # High entropy bin should be first, low entropy txt second
    assert data[0]["path"] == "/app/file_high_entropy.bin", f"Expected high entropy file first, got {data[0]['path']}"
    assert data[1]["path"] == "/app/file_low_entropy.txt", f"Expected low entropy file second, got {data[1]['path']}"

    # Verify PCF is descending
    assert data[0]["pcf"] >= data[1]["pcf"], "Expected PCF to be in descending order"

def test_pcf_computation_logic():
    # Get all 3 items
    resp = requests.get(f"{BASE_URL}/top?n=3")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3

    # Verify exact math for tiny file
    tiny_path = "/app/file_tiny.txt"
    tiny_item = next((item for item in data if item["path"] == tiny_path), None)
    assert tiny_item is not None, f"Could not find {tiny_path} in /top results"

    # Compute expected PCF
    out = subprocess.check_output(["/app/legacy_scorer", tiny_path])
    entropy = float(out.strip())
    size = os.path.getsize(tiny_path)
    expected_pcf = entropy * math.log2(max(size, 2))

    actual_pcf = tiny_item["pcf"]
    assert math.isclose(actual_pcf, expected_pcf, rel_tol=1e-3), \
        f"PCF computation mismatch for {tiny_path}. Expected ~{expected_pcf}, got {actual_pcf}"