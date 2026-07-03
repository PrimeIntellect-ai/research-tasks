# test_final_state.py
import os
import subprocess
import time
import pytest

def test_admin_users_txt():
    path = "/home/user/admin_users.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["alice", "bob", "charlie"]
    assert lines == expected, f"Contents of {path} are incorrect. Expected {expected}, got {lines}"

def test_port_forward_exists():
    path = "/home/user/port_forward.py"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_automate_exp_exists_and_executable():
    path = "/home/user/automate.exp"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_integration_port_forward_and_expect():
    legacy_service_path = "/home/user/legacy_service.py"
    port_forward_path = "/home/user/port_forward.py"
    automate_exp_path = "/home/user/automate.exp"

    # Start legacy service
    legacy_proc = subprocess.Popen([legacy_service_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start port forwarder
    port_forward_proc = subprocess.Popen(["python3", port_forward_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give them a moment to start listening
    time.sleep(1)

    try:
        # Run expect script
        expect_proc = subprocess.run([automate_exp_path], capture_output=True, text=True, timeout=5)

        assert expect_proc.returncode == 0, f"Expect script failed with return code {expect_proc.returncode}. stdout: {expect_proc.stdout}, stderr: {expect_proc.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Expect script timed out. It might be hanging waiting for input or output.")
    finally:
        # Clean up processes
        legacy_proc.terminate()
        port_forward_proc.terminate()
        legacy_proc.wait()
        port_forward_proc.wait()