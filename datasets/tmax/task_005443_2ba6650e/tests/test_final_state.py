# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_server_valid_request():
    url = "http://127.0.0.1:8080/process"
    payload = b'\x01\x41\x42\x00\x00\x00\x00\x05'
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or send request: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("version") == 1
    assert data.get("device_id") == "AB"
    assert data.get("metric") == 5

def test_server_corrupted_request():
    url = "http://127.0.0.1:8080/process"
    payload = b'\x01\x41\xFF\x00\x00\x00\x00\x05'
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or send request: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. The server might have crashed or returned 500."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("version") == 1
    assert data.get("device_id") == "A?", f"Expected device_id to be 'A?', got '{data.get('device_id')}'"
    assert data.get("metric") == 5

def test_rust_unit_test_added():
    repo_path = "/home/user/telemetry_svc"
    main_rs = os.path.join(repo_path, "src", "main.rs")

    assert os.path.exists(main_rs), f"Missing main.rs at {main_rs}"

    with open(main_rs, "r") as f:
        content = f.read()

    assert "#[test]" in content, "No Rust unit test found in src/main.rs (missing #[test] attribute)"

    proc = subprocess.run(["cargo", "test"], cwd=repo_path, capture_output=True, text=True)
    assert proc.returncode == 0, f"cargo test failed:\n{proc.stdout}\n{proc.stderr}"