# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

def test_health_check_exists_and_executable():
    """Test that health_check.sh exists and is executable."""
    path = "/home/user/health_check.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_service_and_health_check_behavior():
    """Test the service behavior, stale PID handling, and health check logic."""
    pid_file = "/home/user/service/run/service.pid"
    status_file = "/home/user/service/data/status.txt"
    start_script = "/home/user/service/start_service.sh"
    health_script = "/home/user/health_check.sh"

    # 1. Verify initial health check (service should be running and healthy)
    result = subprocess.run(["bash", health_script], capture_output=True, text=True)
    assert result.returncode == 0, f"health_check.sh exited with code {result.returncode}, expected 0."
    assert result.stdout.strip() == "HEALTHY", f"health_check.sh output was '{result.stdout.strip()}', expected 'HEALTHY'."

    # 2. Test stale lock handling
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"
    pid = int(pid_str)

    # Kill the running service to create a stale PID scenario
    try:
        os.kill(pid, 9)
    except ProcessLookupError:
        pass

    time.sleep(0.5) # Wait a moment to ensure process is dead

    # Start the service again in the background
    proc = subprocess.Popen(["bash", start_script])
    time.sleep(1) # Give it time to initialize and overwrite PID/status

    # Check health again to ensure it successfully handled the stale PID
    result2 = subprocess.run(["bash", health_script], capture_output=True, text=True)
    assert result2.returncode == 0, "Service failed to start or health_check failed after stale PID recovery."
    assert result2.stdout.strip() == "HEALTHY", "Service is not HEALTHY after recovering from stale PID."

    # 3. Check health_check.sh failure mode
    with open(status_file, "w") as f:
        f.write("INACTIVE\n")

    result3 = subprocess.run(["bash", health_script], capture_output=True, text=True)
    assert result3.returncode == 1, f"health_check.sh should exit with 1 when status is not ACTIVE, got {result3.returncode}."
    assert result3.stdout.strip() == "UNHEALTHY", f"health_check.sh should output UNHEALTHY, got '{result3.stdout.strip()}'."

    # Cleanup: kill the process we spawned during the test
    try:
        with open(pid_file, "r") as f:
            new_pid = int(f.read().strip())
        os.kill(new_pid, 9)
    except Exception:
        pass
    if proc.poll() is None:
        proc.kill()