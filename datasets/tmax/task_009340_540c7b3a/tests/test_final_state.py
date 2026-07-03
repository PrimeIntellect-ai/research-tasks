# test_final_state.py

import os
import subprocess
import time
import pytest

def test_venv_exists():
    """Test that the Python 3 virtual environment is set up."""
    python_path = "/home/user/venv/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment Python not found at {python_path}"

def test_files_created():
    """Test that the required files are created."""
    assert os.path.isfile("/home/user/modern_vm.py"), "modern_vm.py is missing."
    assert os.path.isfile("/home/user/start_server.sh"), "start_server.sh is missing."

def test_server_and_vm_logic():
    """Test that the server starts, and the VM logic correctly processes the bytecode."""
    # Ensure start_server.sh is executable
    os.chmod("/home/user/start_server.sh", 0o755)

    # Run the start_server script
    subprocess.run(["/bin/bash", "/home/user/start_server.sh"], check=True)

    # Give the server a moment to start
    time.sleep(2)

    # Check if PID file was created
    pid_file = "/home/user/vm.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} was not created by start_server.sh"

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer PID: {pid_str}"
    pid = int(pid_str)

    # Verify process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")

    # Run the verification script using the venv's python (which has websockets installed)
    verify_script = "/home/user/verify.py"
    venv_python = "/home/user/venv/bin/python"

    assert os.path.isfile(verify_script), f"Verification script {verify_script} is missing."

    try:
        result = subprocess.run(
            [venv_python, verify_script],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.strip() + "\n" + result.stderr.strip()

        assert result.returncode == 0, f"Verification failed. Output:\n{output}"
        assert "SUCCESS" in output, f"Expected SUCCESS in output, got:\n{output}"

    finally:
        # Cleanup: kill the server
        try:
            os.kill(pid, 15) # SIGTERM
        except OSError:
            pass