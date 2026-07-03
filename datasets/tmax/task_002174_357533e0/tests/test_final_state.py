# test_final_state.py

import os
import subprocess
import time
import urllib.request
import pytest

def test_modproxy_binary():
    """
    Tests that the modproxy binary was successfully built to the correct location,
    binds to port 8080, and responds to /health.
    """
    bin_path = "/home/user/modproxy-bin"
    assert os.path.isfile(bin_path), f"Fixed proxy binary not found at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Binary at {bin_path} is not executable"

    # Run the binary
    proc = subprocess.Popen([bin_path])
    time.sleep(1)  # Allow time for the server to start

    try:
        assert proc.poll() is None, "modproxy-bin crashed or exited immediately. Check if it successfully binds to port 8080."

        req = urllib.request.Request("http://localhost:8080/health")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, f"Expected status 200, got {response.status}"
                body = response.read().decode().strip()
                assert body == "OK", f"Expected body 'OK', got {body}"
        except Exception as e:
            pytest.fail(f"Failed to connect to modproxy-bin on port 8080: {e}. Ensure the perturbation was fixed.")
    finally:
        proc.terminate()
        proc.wait(timeout=2)

def test_e2e_script_and_classification_log():
    """
    Verifies the e2e script exists and runs successfully.
    Then parses the classification log to ensure 100% of EVIL files are rejected
    and 100% of CLEAN files are preserved.
    """
    script_path = "/home/user/run_e2e.sh"
    log_path = "/home/user/classification.log"

    # If the script exists, we run it to generate/overwrite the log
    if os.path.exists(script_path):
        if os.path.exists(log_path):
            os.remove(log_path)

        try:
            subprocess.run(["bash", script_path], timeout=15, check=True)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Execution of {script_path} timed out after 15 seconds.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Execution of {script_path} failed with exit code {e.returncode}.")

    assert os.path.isfile(log_path), f"Classification log not found at {log_path}. Ensure your classifier writes to it."

    with open(log_path, "r") as f:
        log_lines = [line.strip() for line in f if line.strip()]

    log_dict = {}
    for line in log_lines:
        parts = line.split(":")
        if len(parts) >= 2:
            fname = parts[0].strip()
            res = parts[1].strip()
            log_dict[fname] = res

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = os.listdir(clean_dir) if os.path.exists(clean_dir) else []
    evil_files = os.listdir(evil_dir) if os.path.exists(evil_dir) else []

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        if log_dict.get(cf) != "CLEAN":
            clean_modified.append(cf)

    for ef in evil_files:
        if log_dict.get(ef) != "EVIL":
            evil_bypassed.append(ef)

    err_msgs = []
    if evil_bypassed:
        err_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        err_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))