# test_final_state.py

import os
import subprocess
import pytest

def test_result_log():
    log_path = "/home/user/result.log"
    assert os.path.exists(log_path), f"{log_path} does not exist"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SECURE_SERVER_OK", f"Expected 'SECURE_SERVER_OK' in {log_path}, got '{content}'"

def test_server_binary():
    bin_path = "/home/user/app/server"
    assert os.path.isfile(bin_path), f"{bin_path} does not exist"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable"

def test_service_active():
    env = os.environ.copy()
    if "XDG_RUNTIME_DIR" not in env:
        uid = os.getuid()
        env["XDG_RUNTIME_DIR"] = f"/run/user/{uid}"

    try:
        res = subprocess.run(
            ["systemctl", "--user", "is-active", "secure-backend.service"], 
            capture_output=True, text=True, env=env
        )
        assert res.stdout.strip() == "active", f"secure-backend.service is not active. Output: {res.stdout.strip()}"
    except FileNotFoundError:
        pytest.fail("systemctl command not found")

def test_ssh_tunnel_running():
    res = subprocess.run(["pgrep", "-f", "ssh.*-L.*8443.*4433"], capture_output=True, text=True)
    assert res.returncode == 0, "SSH tunnel process forwarding port 8443 to 4433 not found"
    pids = [pid for pid in res.stdout.strip().split('\n') if pid]
    assert len(pids) >= 1, "No SSH tunnel processes found"

def test_setup_script_idempotent():
    script_path = "/home/user/setup.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    try:
        subprocess.run([script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"setup.sh failed on execution. stderr: {e.stderr}")

    res = subprocess.run(["pgrep", "-f", "ssh.*-L.*8443.*4433"], capture_output=True, text=True)
    pids = [pid for pid in res.stdout.strip().split('\n') if pid]

    assert len(pids) == 1, f"Idempotency failed: Expected exactly 1 SSH tunnel process, found {len(pids)}"