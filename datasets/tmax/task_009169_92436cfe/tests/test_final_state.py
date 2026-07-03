# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

SUPERVISE_SCRIPT = "/home/user/planner/supervise.sh"
SOCKET_LINK = "/home/user/planner/run/socket"
EXPECTED_TARGET = "/home/user/app/metrics.sock"
LOG_DIR = "/home/user/planner/logs"

@pytest.fixture(scope="session", autouse=True)
def run_supervisor():
    """Run the student's supervise.sh script to generate the final state."""
    assert os.path.isfile(SUPERVISE_SCRIPT), f"{SUPERVISE_SCRIPT} does not exist."

    # Check if executable
    st = os.stat(SUPERVISE_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SUPERVISE_SCRIPT} is not executable."

    # Run the script in the background
    proc = subprocess.Popen(["/bin/bash", SUPERVISE_SCRIPT])

    # Let it run long enough to trigger multiple crashes and rotations (0.5s per run)
    time.sleep(4)

    # Terminate the supervisor
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()

    # Also kill any lingering analyzer processes
    subprocess.run(["pkill", "-f", "python3 /home/user/analyzer.py"], capture_output=True)

    yield

def test_directories_exist():
    """Check if the required directories were created."""
    dirs = [
        "/home/user/planner/run",
        "/home/user/planner/logs",
        "/home/user/app"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Required directory {d} does not exist."

def test_symlink_correctness():
    """Check if the socket symlink is correct."""
    assert os.path.islink(SOCKET_LINK), f"{SOCKET_LINK} is not a symlink."
    target = os.readlink(SOCKET_LINK)
    assert target == EXPECTED_TARGET, f"Symlink points to {target}, expected {EXPECTED_TARGET}."

def test_log_rotation():
    """Check if log rotation created the expected historical logs with correct content."""
    for i in range(1, 4):
        log_file = os.path.join(LOG_DIR, f"analyzer.log.{i}")
        assert os.path.isfile(log_file), f"Rotated log file {log_file} does not exist. Ensure the loop restarts and rotates logs."

        with open(log_file, "r") as f:
            content = f.read()
            assert "Analyzer started successfully" in content, f"Log {log_file} does not contain expected output."
            assert "Fatal: Simulated OOM exception." in content, f"Log {log_file} does not contain the crash message."