# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

def test_alert_monitor_service_content():
    """Verify the modifications to alert-monitor.service."""
    file_path = "/home/user/monitoring/alert-monitor.service"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    # Find the [Unit] section and check if the required lines are present
    assert "[Unit]" in content, "Missing [Unit] section in alert-monitor.service"

    # Simple check for the required lines
    assert "After=log-aggregator.service" in content, "Missing 'After=log-aggregator.service' in alert-monitor.service"
    assert "Requires=log-aggregator.service" in content, "Missing 'Requires=log-aggregator.service' in alert-monitor.service"

def test_setup_env_script():
    """Verify setup-env.sh exists, is executable, and performs correctly."""
    script_path = "/home/user/monitoring/setup-env.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute properly."

    # Verify directories
    logs_dir = "/home/user/monitoring/logs"
    active_alerts_dir = "/home/user/monitoring/alerts/active"
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} was not created."
    assert os.path.isdir(active_alerts_dir), f"Directory {active_alerts_dir} was not created."

    # Verify symlink
    symlink_path = "/home/user/monitoring/latest_alert_dir"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    assert target == active_alerts_dir, f"Symlink {symlink_path} points to {target} instead of {active_alerts_dir}."

def test_check_process_script():
    """Verify check-process.sh exists, is executable, and works correctly."""
    script_path = "/home/user/monitoring/check-process.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Ensure dummy-aggregator is NOT running
    subprocess.run(["pkill", "-f", "dummy-aggregator"])
    time.sleep(0.5)

    # Run script when missing
    result_missing = subprocess.run([script_path], capture_output=True, text=True)
    assert result_missing.returncode == 1, f"Expected exit code 1 when process is missing, got {result_missing.returncode}."
    assert result_missing.stdout.strip() == "Aggregator is missing", f"Expected output 'Aggregator is missing', got '{result_missing.stdout.strip()}'."

    # Start dummy-aggregator
    dummy_proc = subprocess.Popen(["bash", "-c", "exec -a dummy-aggregator sleep 10"])
    time.sleep(0.5)

    try:
        # Run script when running
        result_running = subprocess.run([script_path], capture_output=True, text=True)
        assert result_running.returncode == 0, f"Expected exit code 0 when process is running, got {result_running.returncode}."
        assert result_running.stdout.strip() == "Aggregator is running", f"Expected output 'Aggregator is running', got '{result_running.stdout.strip()}'."
    finally:
        # Cleanup
        dummy_proc.terminate()
        dummy_proc.wait()