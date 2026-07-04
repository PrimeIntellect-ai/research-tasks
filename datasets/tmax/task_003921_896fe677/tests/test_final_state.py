# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_directory_and_symlink():
    """Verify the directory structure and symlink for telemetry data."""
    dir_path = "/home/user/iot_gateway/telemetry/node_01"
    symlink_path = "/home/user/iot_gateway/current_node"

    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    assert target == dir_path, f"Symlink {symlink_path} points to {target}, expected {dir_path}."

def test_socat_port_forwarding():
    """Verify that socat is running and listening on port 8443."""
    # Check if socat process is running
    try:
        subprocess.run(["pgrep", "-x", "socat"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        pytest.fail("socat process is not running.")

    # Check if port 8443 is listening
    try:
        result = subprocess.run(["ss", "-tln"], check=True, stdout=subprocess.PIPE, text=True)
        assert ":8443" in result.stdout, "Port 8443 is not listening."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ss command to check listening ports.")

def test_diagnostics_script():
    """Verify that the diagnostics script exists and is executable."""
    script_path = "/home/user/iot_gateway/diagnostics.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_health_log_content_and_permissions():
    """Verify the health log content and its permissions."""
    log_path = "/home/user/iot_gateway/health.log"

    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()
    assert "OK_FORWARDING" in content, f"Log file {log_path} does not contain 'OK_FORWARDING'."

    # Check permissions (644)
    file_stat = os.stat(log_path)
    perms = stat.S_IMODE(file_stat.st_mode)
    assert perms == 0o644, f"Permissions for {log_path} are {oct(perms)}, expected 0o644."