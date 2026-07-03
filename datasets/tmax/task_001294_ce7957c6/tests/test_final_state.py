# test_final_state.py

import os
import subprocess
import time
import socket
import pytest

def test_files_exist_and_executable():
    """Check that bridge.py and test_pipeline.sh exist, and the script is executable."""
    assert os.path.isfile("/home/user/bridge.py"), "/home/user/bridge.py does not exist."
    assert os.path.isfile("/home/user/test_pipeline.sh"), "/home/user/test_pipeline.sh does not exist."
    assert os.access("/home/user/test_pipeline.sh", os.X_OK), "/home/user/test_pipeline.sh is not executable."

def test_pipeline_script_execution():
    """Run the test_pipeline.sh script and verify its output and cleanup."""
    # Ensure any previous run's log is removed
    log_file = "/home/user/dashboard_output.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    # Run the script
    result = subprocess.run(
        ["/home/user/test_pipeline.sh"],
        cwd="/home/user",
        capture_output=True,
        text=True,
        timeout=30
    )

    assert result.returncode == 0, f"test_pipeline.sh failed with return code {result.returncode}. Stderr: {result.stderr}"

    # Check output log
    assert os.path.isfile(log_file), f"{log_file} was not created by test_pipeline.sh."
    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == "CI_BUILD_SUCCESS", f"Expected 'CI_BUILD_SUCCESS' in {log_file}, got '{content}'."

def test_ports_cleaned_up():
    """Ensure no processes are left listening on ports 50051 or 8765."""
    # Give it a tiny bit of time to clean up if needed
    time.sleep(1)

    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    assert not is_port_in_use(50051), "Port 50051 is still in use. bridge.py was not properly cleaned up."
    assert not is_port_in_use(8765), "Port 8765 is still in use. bridge.py was not properly cleaned up."