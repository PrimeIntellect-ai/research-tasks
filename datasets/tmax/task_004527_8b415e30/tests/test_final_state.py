# test_final_state.py

import os
import socket
import requests
import subprocess
import json

def test_bad_commit_reported():
    bad_commit_file = "/app/bad_commit.txt"
    secret_file = "/tmp/secret_bad_commit.txt"

    assert os.path.exists(bad_commit_file), f"Missing {bad_commit_file}. Did you write the bad commit SHA?"
    assert os.path.exists(secret_file), f"Missing {secret_file} (test harness issue)."

    with open(bad_commit_file, "r") as f:
        reported_commit = f.read().strip()

    with open(secret_file, "r") as f:
        actual_commit = f.read().strip()

    assert reported_commit == actual_commit, f"Reported bad commit '{reported_commit}' does not match the actual bad commit."

def test_backend_repo_on_main():
    result = subprocess.run(
        ["git", "-C", "/app/backend", "branch", "--show-current"], 
        capture_output=True, 
        text=True
    )
    current_branch = result.stdout.strip()
    assert current_branch == "main", f"Backend repository is on branch '{current_branch}', expected 'main'."

def test_backend_service_tcp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0)
        s.connect(('127.0.0.1', 9090))
        s.sendall(b'ping\n')
        data = s.recv(1024).decode('utf-8')
        s.close()
    except Exception as e:
        assert False, f"Failed to connect and communicate with backend on TCP port 9090: {e}"

    assert data.strip() == "pong", f"Expected backend to respond with 'pong', got '{data.strip()}'"

def test_frontend_service_http():
    try:
        response = requests.get("http://127.0.0.1:8080/status", timeout=3.0)
    except Exception as e:
        assert False, f"Failed to connect to frontend on HTTP port 8080: {e}"

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"

    try:
        json_data = response.json()
    except ValueError:
        assert False, f"Frontend response is not valid JSON. Response body: {response.text}"

    assert json_data.get("status") == "ok", f"Expected 'status': 'ok' in JSON response, got: {json_data.get('status')}"
    assert json_data.get("backend_data") == 45, f"Expected 'backend_data': 45 in JSON response, got: {json_data.get('backend_data')}"