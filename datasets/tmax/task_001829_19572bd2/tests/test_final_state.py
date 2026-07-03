# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_status_file_ready():
    status_file = "/home/user/status.txt"
    assert os.path.isfile(status_file), f"Status file {status_file} is missing."
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected status file to contain 'READY', but got '{content}'"

def test_cargo_tests_pass():
    repo_dir = "/home/user/audioproxy"
    assert os.path.isdir(repo_dir), f"Directory {repo_dir} does not exist"

    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("cargo test timed out")

def test_proxy_valid_request():
    url = "http://127.0.0.1:8080/secure-entry"
    headers = {"X-Audio-Passphrase": "delta protocol active"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

        json_data = response.json()
        assert json_data.get("status") == "granted", f"Expected JSON {{'status': 'granted'}}, got {json_data}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy: {e}")

def test_proxy_invalid_request_wrong_passphrase():
    url = "http://127.0.0.1:8080/secure-entry"
    headers = {"X-Audio-Passphrase": "wrong password"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized for wrong passphrase, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy: {e}")

def test_proxy_invalid_request_missing_header():
    url = "http://127.0.0.1:8080/secure-entry"

    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized for missing header, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy: {e}")