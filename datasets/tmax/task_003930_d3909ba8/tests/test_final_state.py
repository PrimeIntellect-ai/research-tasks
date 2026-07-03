# test_final_state.py

import os
import subprocess
import tempfile
import socket
import time
import requests
import pytest

def test_git_repo_and_hook():
    repo_path = "/home/user/vm-specs.git"
    assert os.path.exists(repo_path), f"Bare git repository not found at {repo_path}"
    assert os.path.isdir(os.path.join(repo_path, "refs")), f"{repo_path} does not look like a bare git repository"

    hook_path = os.path.join(repo_path, "hooks", "pre-receive")
    assert os.path.exists(hook_path), f"pre-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook at {hook_path} is not executable"

def test_systemd_service_running():
    # Check if the service is active
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "cap-server"],
            capture_output=True, text=True, check=False,
            env=dict(os.environ, XDG_RUNTIME_DIR="/run/user/1000")
        )
        assert result.stdout.strip() == "active", "cap-server systemd user service is not active"
    except Exception as e:
        pytest.fail(f"Failed to check systemd service: {e}")

def test_http_verify_endpoint():
    url = "http://127.0.0.1:8080/verify"

    # Valid payload
    valid_payload = {"ram_mb": 2048, "cpu_cores": 2}
    try:
        resp = requests.post(url, json=valid_payload, timeout=5)
        assert resp.status_code == 200, f"Expected 200 OK for valid verify, got {resp.status_code}"
        assert resp.text.strip() == "OK", f"Expected 'OK' for valid verify, got '{resp.text.strip()}'"
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    # Invalid payload
    invalid_payload = {"ram_mb": 16384, "cpu_cores": 8}
    try:
        resp = requests.post(url, json=invalid_payload, timeout=5)
        assert resp.status_code == 200, f"Expected 200 OK for invalid verify, got {resp.status_code}"
        assert resp.text.strip() == "REJECT", f"Expected 'REJECT' for invalid verify, got '{resp.text.strip()}'"
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

def test_http_allocate_endpoint_and_qemu():
    url = "http://127.0.0.1:8080/allocate"

    # Invalid payload should be rejected and return 400
    invalid_payload = {"ram_mb": 16384, "cpu_cores": 8}
    try:
        resp = requests.post(url, json=invalid_payload, timeout=5)
        assert resp.status_code == 400, f"Expected 400 Bad Request for invalid allocate, got {resp.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    # Valid payload should allocate and start QEMU
    valid_payload = {"ram_mb": 2048, "cpu_cores": 2}
    try:
        resp = requests.post(url, json=valid_payload, timeout=5)
        assert resp.status_code == 200, f"Expected 200 OK for valid allocate, got {resp.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    # Verify QEMU is running and listening on VNC port 5901
    time.sleep(1) # Give QEMU a moment to start
    vnc_port = 5901
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', vnc_port))
        assert result == 0, f"QEMU does not seem to be listening on VNC port {vnc_port}"

def test_git_push_behavior():
    repo_path = "/home/user/vm-specs.git"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        subprocess.run(["git", "clone", repo_path, tmpdir], check=True, capture_output=True)

        # Configure git
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)

        # Test valid push
        valid_file = os.path.join(tmpdir, "valid.json")
        with open(valid_file, "w") as f:
            f.write('{"ram_mb": 2048, "cpu_cores": 2}')
        subprocess.run(["git", "add", "valid.json"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Add valid spec"], cwd=tmpdir, check=True)

        push_valid = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert push_valid.returncode == 0, f"Git push failed for valid JSON. Output: {push_valid.stderr}"

        # Test invalid push
        invalid_file = os.path.join(tmpdir, "invalid.json")
        with open(invalid_file, "w") as f:
            f.write('{"ram_mb": 16384, "cpu_cores": 8}')
        subprocess.run(["git", "add", "invalid.json"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Add invalid spec"], cwd=tmpdir, check=True)

        push_invalid = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert push_invalid.returncode != 0, "Git push succeeded for invalid JSON, but it should have been rejected."
        assert "REJECT" in push_invalid.stderr or "declined" in push_invalid.stderr, "Git push rejection did not contain expected hook output."