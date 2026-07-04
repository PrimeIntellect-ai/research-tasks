# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

def test_nginx_conf_fixed():
    conf_path = "/home/user/finops-scale/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."
    with open(conf_path, "r") as f:
        content = f.read()
    expected_path = "proxy_pass http://unix:/home/user/finops-scale/sockets/app.sock;"
    assert expected_path in content, f"nginx.conf does not contain the correct proxy_pass directive. Expected it to contain: {expected_path}"

def test_finops_users_created():
    users_path = "/home/user/finops-scale/finops-users.txt"
    assert os.path.isfile(users_path), f"File {users_path} is missing."
    with open(users_path, "r") as f:
        content = f.read().strip()
    expected_line = "cost-saver:finops-admin:active"
    assert content == expected_line, f"finops-users.txt content is incorrect. Expected '{expected_line}', got '{content}'."

def test_worker_fstab_created():
    fstab_path = "/home/user/finops-scale/worker-fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} is missing."
    with open(fstab_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    assert len(lines) == 1, "worker-fstab should contain exactly one non-comment line."
    parts = lines[0].split()
    assert len(parts) == 6, f"worker-fstab entry should have exactly 6 fields, found {len(parts)}."

    assert parts[0] == "/home/user/data-disk.img", f"Incorrect device/file path: {parts[0]}"
    assert parts[1] == "/home/user/finops-scale/shared_data", f"Incorrect mount point: {parts[1]}"
    assert parts[2] == "ext4", f"Incorrect filesystem type: {parts[2]}"
    assert parts[3] == "loop,ro", f"Incorrect mount options: {parts[3]}"
    assert parts[4] == "0", f"Incorrect dump field: {parts[4]}"
    assert parts[5] == "0", f"Incorrect pass field: {parts[5]}"

def test_scaler_script_behavior():
    script_path = "/home/user/finops-scale/scaler.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    # Check if executable
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"{script_path} is not executable."

    log_path = "/home/user/finops-scale/metrics.log"
    worker_path = "/home/user/finops-scale/mock-worker.py"

    # Ensure the worker script exists
    assert os.path.isfile(worker_path), f"Worker script {worker_path} missing."

    proc = None
    try:
        # Test 1: STATUS:BUSY - should not kill
        with open(log_path, "w") as f:
            f.write("STATUS:BUSY\n")

        proc = subprocess.Popen(["python3", worker_path])
        time.sleep(0.5) # Allow process to start

        result = subprocess.run([script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"scaler.sh exited with non-zero status when metrics.log was STATUS:BUSY."

        time.sleep(0.5)
        assert proc.poll() is None, "scaler.sh improperly killed the worker process when status was BUSY."

        # Test 2: STATUS:IDLE - should kill
        with open(log_path, "w") as f:
            f.write("STATUS:IDLE\n")

        result = subprocess.run([script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"scaler.sh exited with non-zero status when metrics.log was STATUS:IDLE."

        time.sleep(0.5) # Allow time for signal to process
        assert proc.poll() is not None, "scaler.sh failed to kill the worker process when status was IDLE."

    finally:
        # Cleanup if process is still running
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait()