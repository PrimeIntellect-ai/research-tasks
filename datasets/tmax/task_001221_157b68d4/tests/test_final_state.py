# test_final_state.py

import os
import subprocess
import socket
import time
import pytest

def test_health_checker_exists_and_executable():
    """Verify that the compiled health_checker exists and is executable."""
    checker_path = "/home/user/health_checker"
    assert os.path.exists(checker_path), f"{checker_path} does not exist."
    assert os.path.isfile(checker_path), f"{checker_path} is not a file."
    assert os.access(checker_path, os.X_OK), f"{checker_path} is not executable."

def test_health_checker_behavior():
    """Verify the health_checker binary exits with correct codes."""
    checker_path = "/home/user/health_checker"

    # Port 8081 should be UP
    result_up = subprocess.run([checker_path, "8081"], capture_output=True)
    assert result_up.returncode == 0, f"Expected exit code 0 for port 8081, got {result_up.returncode}"

    # Find a free port for DOWN test
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        free_port = s.getsockname()[1]

    result_down = subprocess.run([checker_path, str(free_port)], capture_output=True)
    assert result_down.returncode == 1, f"Expected exit code 1 for closed port {free_port}, got {result_down.returncode}"

def test_monitor_sh_behavior():
    """Verify monitor.sh script logic."""
    monitor_path = "/home/user/monitor.sh"
    log_path = "/home/user/health.log"

    assert os.path.exists(monitor_path), f"{monitor_path} does not exist."
    assert os.access(monitor_path, os.X_OK), f"{monitor_path} is not executable."

    # Ensure log is clean for testing
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run monitor.sh while service is UP
    subprocess.run([monitor_path], check=True)

    assert os.path.exists(log_path), f"{log_path} was not created."
    with open(log_path, "r") as f:
        lines = f.readlines()
    assert len(lines) >= 1, "Log file is empty."
    assert lines[-1] == "UP\n", f"Expected last line to be 'UP\\n', got {repr(lines[-1])}"

    # Kill the python server to test DOWN state
    # Find the process listening on 8081
    try:
        pid_output = subprocess.check_output(["lsof", "-t", "-i", ":8081"]).decode().strip()
        if pid_output:
            for pid in pid_output.split():
                subprocess.run(["kill", "-9", pid])
            time.sleep(0.5)
    except Exception:
        pass # If lsof fails or no process found, ignore

    # Run monitor.sh while service is DOWN
    subprocess.run([monitor_path], check=False)

    with open(log_path, "r") as f:
        lines = f.readlines()
    assert len(lines) >= 2, "Log file did not append new status."
    assert lines[-1] == "DOWN\n", f"Expected last line to be 'DOWN\\n', got {repr(lines[-1])}"

def test_cron_job():
    """Verify the cron job is installed for the user account."""
    try:
        # We run crontab -l as the current user (assuming tests run as the target user or root checking 'user')
        # Since the prompt says "user-level cron job for the 'user' account", let's check for 'user'
        result = subprocess.run(["crontab", "-u", "user", "-l"], capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback to current user if -u fails
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)

        assert result.returncode == 0, "Failed to read crontab."

        cron_lines = [line.strip() for line in result.stdout.split('\n') if line.strip() and not line.startswith('#')]

        found = False
        for line in cron_lines:
            parts = line.split()
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = " ".join(parts[5:])
                if schedule == "* * * * *" and "/home/user/monitor.sh" in command:
                    found = True
                    break

        assert found, "Could not find cron entry matching '* * * * * /home/user/monitor.sh'"
    except FileNotFoundError:
        pytest.fail("crontab command not found")