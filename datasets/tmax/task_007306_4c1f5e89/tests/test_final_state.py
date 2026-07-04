# test_final_state.py

import os
import re
import time
import signal
import subprocess
import pytest

def test_environment_variables():
    """Verify that the environment variables were appended to .profile."""
    profile_path = "/home/user/.profile"
    assert os.path.exists(profile_path), f"{profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    assert "MIGRATION_PHASE=hybrid" in content, "MIGRATION_PHASE=hybrid not found in .profile"
    assert "QEMU_VNC_DISPLAY=:5" in content, "QEMU_VNC_DISPLAY=:5 not found in .profile"

def test_qemu_running():
    """Verify that qemu-system-x86_64 is running with the correct arguments."""
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command.")

    qemu_processes = [line for line in output.splitlines() if "qemu-system-x86_64" in line and not "grep" in line]
    assert qemu_processes, "qemu-system-x86_64 is not running."

    found_vnc = False
    found_serial = False
    for process in qemu_processes:
        if "-vnc :5" in process or "-vnc" in process and ":5" in process:
            found_vnc = True
        if "-serial file:/home/user/legacy_vm.log" in process:
            found_serial = True

    assert found_vnc, "QEMU is not running with VNC display :5."
    assert found_serial, "QEMU is not running with serial redirect to /home/user/legacy_vm.log."

def test_logrotate_config():
    """Verify the logrotate configuration file contains the required rules."""
    config_path = "/home/user/vm_logrotate.conf"
    assert os.path.exists(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert re.search(r'\bhourly\b', content), "Rule 'hourly' not found in logrotate config."
    assert re.search(r'\brotate\s+5\b', content), "Rule 'rotate 5' not found in logrotate config."
    assert re.search(r'\bcompress\b', content), "Rule 'compress' not found in logrotate config."
    assert re.search(r'\bmissingok\b', content), "Rule 'missingok' not found in logrotate config."

def test_logrotate_status():
    """Verify that logrotate was run by checking the status file."""
    status_path = "/home/user/logrotate.status"
    assert os.path.exists(status_path), f"{status_path} does not exist. Did logrotate run?"

def test_container_shim_lifecycle():
    """Verify the container shim script logic and lifecycle handling."""
    pid_file = "/home/user/container_shim.pid"
    assert os.path.exists(pid_file), f"{pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID."
    pid = int(pid_str)

    # Check process is actually running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

    log_file = "/home/user/nextgen.log"
    assert os.path.exists(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "[INFO] Starting next-gen service" in log_content, "Startup log message not found."

    # Send SIGTERM
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pytest.fail(f"Failed to send SIGTERM to process {pid}.")

    # Wait for trap to process
    time.sleep(1.5)

    # Check if process exited
    process_running = True
    try:
        os.kill(pid, 0)
    except OSError:
        process_running = False

    assert not process_running, f"Process {pid} did not exit after receiving SIGTERM."

    # Check shutdown log
    with open(log_file, "r") as f:
        log_content = f.read()

    assert "[INFO] Shutting down gracefully" in log_content, "Shutdown log message not found."