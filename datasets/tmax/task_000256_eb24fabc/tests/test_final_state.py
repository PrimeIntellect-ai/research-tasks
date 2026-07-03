# test_final_state.py

import os
import re
import stat
import time
import subprocess
import requests

def test_authorized_keys_permissions():
    path = "/home/user/.ssh/authorized_keys"
    assert os.path.exists(path), f"{path} does not exist"
    st = os.stat(path)
    assert not bool(st.st_mode & stat.S_IWOTH), "authorized_keys is still world-writable"
    assert not bool(st.st_mode & stat.S_IWGRP), "authorized_keys is still group-writable"

def test_router_config_fixed():
    path = "/home/user/app/router/routes.conf"
    assert os.path.exists(path), f"{path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "backend=127.0.0.1:9090" in content, "The routing bug in routes.conf has not been fixed to point to 127.0.0.1:9090"

def test_health_log_exists_and_format():
    path = "/home/user/health.log"
    assert os.path.exists(path), f"{path} does not exist. Health check script may not be running."

    with open(path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "health.log is empty"

    last_line = lines[-1].strip()
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] STATUS: 200$"
    assert re.match(pattern, last_line), f"Log entry '{last_line}' does not match expected format or status is not 200"

def test_e2e_ssh_tunnel_and_http():
    # Establish SSH tunnel
    tunnel_cmd = [
        "ssh", "-i", "/home/user/test_key",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-p", "2222",
        "-N", "-L", "8888:127.0.0.1:8080",
        "user@127.0.0.1"
    ]

    proc = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for the tunnel to be established
        time.sleep(2)

        # Check if SSH process died early (e.g., auth failure)
        if proc.poll() is not None:
            _, stderr = proc.communicate()
            assert False, f"SSH tunnel failed to start. stderr: {stderr.decode()}"

        # Make the HTTP request through the tunnel
        try:
            resp = requests.get("http://127.0.0.1:8888/api/status", timeout=5)
        except requests.exceptions.RequestException as e:
            assert False, f"Failed to connect to backend via SSH tunnel: {e}"

        assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}"

        try:
            data = resp.json()
            assert data == {"status": "ok", "service": "backend"}, f"Unexpected response body: {data}"
        except ValueError:
            assert False, f"Response is not valid JSON: {resp.text}"

    finally:
        proc.terminate()
        proc.wait()