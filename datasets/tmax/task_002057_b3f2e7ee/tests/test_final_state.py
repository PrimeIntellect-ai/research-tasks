# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_legacy_sensor_bin_running():
    """Test that the legacy_sensor_bin process is currently running."""
    try:
        # Check if the process is running using pgrep
        result = subprocess.run(
            ["pgrep", "-f", "/home/user/legacy_sensor_bin"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert result.returncode == 0, "legacy_sensor_bin is not running. The watchdog script may not have started it correctly."
    except FileNotFoundError:
        pytest.fail("pgrep command not found. Ensure procps is installed.")

def test_log_rotated():
    """Test that the telemetry log was successfully rotated."""
    rotated_log_path = "/home/user/telemetry.log.1"
    assert os.path.exists(rotated_log_path), (
        f"Rotated log file {rotated_log_path} does not exist. "
        "Log rotation did not occur or was not configured correctly."
    )
    assert os.path.isfile(rotated_log_path), f"{rotated_log_path} is not a regular file."

def test_watchdog_script_exists_and_executable():
    """Test that the watchdog script exists and is executable."""
    watchdog_path = "/home/user/watchdog.sh"
    assert os.path.exists(watchdog_path), f"Watchdog script {watchdog_path} does not exist."
    assert os.path.isfile(watchdog_path), f"{watchdog_path} is not a regular file."

    st = os.stat(watchdog_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Watchdog script {watchdog_path} is not executable."

def test_launcher_expect_script_exists():
    """Test that the launcher expect script exists."""
    launcher_path = "/home/user/launcher.exp"
    assert os.path.exists(launcher_path), f"Expect script {launcher_path} does not exist."
    assert os.path.isfile(launcher_path), f"{launcher_path} is not a regular file."

def test_rotate_conf_exists():
    """Test that the logrotate configuration file exists."""
    rotate_conf_path = "/home/user/rotate.conf"
    assert os.path.exists(rotate_conf_path), f"Logrotate config {rotate_conf_path} does not exist."
    assert os.path.isfile(rotate_conf_path), f"{rotate_conf_path} is not a regular file."

def test_telemetry_log_exists():
    """Test that the active telemetry log exists."""
    log_path = "/home/user/telemetry.log"
    assert os.path.exists(log_path), f"Active log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a regular file."