# test_final_state.py

import os
import stat
import json
import subprocess
import requests
import pytest

def test_fuzz_test_script():
    path = "/home/user/fuzz_test.sh"
    assert os.path.isfile(path), f"Fuzz test script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Fuzz test script {path} is not executable."

def test_cmakelists_rpath():
    path = "/home/user/legacy_audio/CMakeLists.txt"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "RPATH" in content.upper(), "CMakeLists.txt does not seem to contain RPATH configurations."

def get_expected_hash(transcript, seed_phrase):
    # Try to use the built executable if it exists
    cli_path = "/home/user/legacy_audio/build/hasher_cli"
    if not os.path.isfile(cli_path):
        # Fallback: build it ourselves to get the hash
        build_dir = "/tmp/test_build"
        os.makedirs(build_dir, exist_ok=True)
        subprocess.run(["cmake", "/home/user/legacy_audio"], cwd=build_dir, check=True, capture_output=True)
        subprocess.run(["make"], cwd=build_dir, check=True, capture_output=True)
        cli_path = os.path.join(build_dir, "hasher_cli")

    result = subprocess.run([cli_path, transcript, seed_phrase], capture_output=True, text=True, env={"LD_LIBRARY_PATH": ""})
    assert result.returncode == 0, f"hasher_cli failed: {result.stderr}"
    return result.stdout.strip()

def test_http_server_valid_json():
    url = "http://127.0.0.1:9090/hash"
    payload = {"transcript": "hello world"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("Response is not valid JSON")

    assert data.get("status") == "success", "Response JSON missing 'status': 'success'"

    expected_hash = get_expected_hash("hello world", "rusted metal")
    assert data.get("hash") == expected_hash, f"Expected hash '{expected_hash}', got '{data.get('hash')}'"

def test_http_server_invalid_json():
    url = "http://127.0.0.1:9090/hash"
    payload = '{"transcript": "hello world"' # Malformed JSON
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for malformed JSON, got {response.status_code}"