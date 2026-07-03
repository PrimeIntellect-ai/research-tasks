# test_final_state.py

import os
import subprocess
import pytest
import socket

def test_deploy_port_file():
    """Check that the deploy port file contains the correct port."""
    port_file = "/home/user/deploy_port.txt"
    assert os.path.isfile(port_file), f"Missing {port_file}"
    with open(port_file, "r") as f:
        content = f.read().strip()
    assert content == "9002", f"Expected port 9002 in {port_file}, but got {content}"

def test_ssh_tunnel_active():
    """Check that port 8080 is open and listening."""
    # We can check if we can connect to localhost:8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8080))
        s.close()
    except ConnectionRefusedError:
        pytest.fail("SSH tunnel is not listening on local port 8080.")

def test_worker_wrapper():
    """Check that the worker wrapper sets the correct ulimit and executes arguments."""
    wrapper_path = "/home/user/worker_wrapper.sh"
    assert os.path.isfile(wrapper_path), f"Missing {wrapper_path}"
    assert os.access(wrapper_path, os.X_OK), f"{wrapper_path} is not executable"

    try:
        result = subprocess.run(
            [wrapper_path, "sh", "-c", "ulimit -f"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip()
        assert "51200" in output, f"Expected ulimit -f to be 51200, but got: {output}"
    except Exception as e:
        pytest.fail(f"Failed to execute worker wrapper: {e}")

def test_validator_clean_corpus():
    """Check that the validator accepts all clean files."""
    validator_path = "/home/user/validator"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isfile(validator_path), f"Missing validator executable at {validator_path}"
    assert os.access(validator_path, os.X_OK), f"Validator at {validator_path} is not executable"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    failed_files = []

    for filepath in clean_files:
        result = subprocess.run([validator_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected: {', '.join(failed_files)}")

def test_validator_evil_corpus():
    """Check that the validator rejects all evil files."""
    validator_path = "/home/user/validator"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isfile(validator_path), f"Missing validator executable at {validator_path}"
    assert os.access(validator_path, os.X_OK), f"Validator at {validator_path} is not executable"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    failed_files = []

    for filepath in evil_files:
        result = subprocess.run([validator_path, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}")