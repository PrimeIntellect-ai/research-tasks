# test_final_state.py

import os
import subprocess
import stat
import pytest

def test_monitor_binary_exists_and_executable():
    """Verify that the monitor binary was compiled and is executable."""
    binary_path = "/home/user/bin/monitor"
    assert os.path.exists(binary_path), f"Binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_run_monitor_script():
    """Verify the run_monitor.sh script exists, is executable, and runs successfully."""
    script_path = "/home/user/bin/run_monitor.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_monitor.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

    # Verify output file
    log_path = "/home/user/logs/monitor_status.log"
    assert os.path.exists(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"Log file {log_path} is empty."
    assert lines[-1].strip() == "STATUS: OK - /home/user/data", f"Log file {log_path} does not contain the expected success message."

def test_monitor_binary_fallback_behavior():
    """Verify the monitor binary uses the fallback log path when MONITOR_OUTPUT_PATH is not set."""
    binary_path = "/home/user/bin/monitor"
    fallback_log = "/home/user/wrong_logs/fallback.log"

    # Remove fallback log if it exists
    if os.path.exists(fallback_log):
        os.remove(fallback_log)

    env = os.environ.copy()
    env["DATA_DIR"] = "/home/user/data"
    if "MONITOR_OUTPUT_PATH" in env:
        del env["MONITOR_OUTPUT_PATH"]

    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Binary failed when MONITOR_OUTPUT_PATH was unset. Exit code: {result.returncode}"

    assert os.path.exists(fallback_log), f"Fallback log {fallback_log} was not created when MONITOR_OUTPUT_PATH was unset."
    with open(fallback_log, "r") as f:
        content = f.read()
    assert "STATUS: OK - /home/user/data" in content, f"Fallback log does not contain expected message."

def test_health_check_script():
    """Verify the health_check.sh script exists, is executable, and outputs correctly."""
    script_path = "/home/user/bin/health_check.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Ensure log is in healthy state before running
    log_path = "/home/user/logs/monitor_status.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as f:
        f.write("STATUS: OK - /home/user/data\n")

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"health_check.sh failed with exit code {result.returncode}."
    assert result.stdout.strip() == "HEALTHY", f"health_check.sh output '{result.stdout.strip()}' instead of 'HEALTHY'."

def test_bash_profile_configured():
    """Verify that the bash profile has the correct configuration appended."""
    bash_profile = "/home/user/.bash_profile"
    assert os.path.exists(bash_profile), f"{bash_profile} does not exist."

    with open(bash_profile, "r") as f:
        content = f.read()

    assert "export MONITOR_CONFIGURED=true" in content, f"export MONITOR_CONFIGURED=true not found in {bash_profile}"

    # Check if it's exactly on a line
    lines = [line.strip() for line in content.splitlines()]
    assert "export MONITOR_CONFIGURED=true" in lines, f"export MONITOR_CONFIGURED=true must be on its own line in {bash_profile}"