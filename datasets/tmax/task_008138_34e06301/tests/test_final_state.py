# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_run_sh_execution_in_empty_env():
    """Verify that run.sh executes successfully in a completely empty environment."""
    run_script = "/home/user/netmon/run.sh"
    assert os.path.isfile(run_script), f"{run_script} is missing"

    # Run the script with an empty environment
    result = subprocess.run(
        ["env", "-i", "bash", run_script],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run.sh failed to execute in an empty environment. stderr: {result.stderr}"

def test_net_logs_directory_exists_and_permissions():
    """Verify that /home/user/net_logs exists and has strict 750 permissions."""
    log_dir = "/home/user/net_logs"
    assert os.path.isdir(log_dir), f"Directory {log_dir} is missing"

    # Check permissions
    st = os.stat(log_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o750, f"Directory {log_dir} permissions are {oct(perms)}, expected 0o750"

def test_log_file_created_and_content():
    """Verify that status.log is created in the correct directory with the expected content."""
    log_file = "/home/user/net_logs/status.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing"

    with open(log_file, "r") as f:
        content = f.read()

    assert "STATUS: 8080_CLOSED" in content, f"Incorrect or missing content in {log_file}. Found: {content}"

def test_go_script_reads_env_var():
    """Verify that monitor.go was modified to read NET_LOG_DIR."""
    go_file = "/home/user/netmon/monitor.go"
    assert os.path.isfile(go_file), f"{go_file} is missing"

    with open(go_file, "r") as f:
        content = f.read()

    assert "NET_LOG_DIR" in content, "monitor.go does not appear to read the NET_LOG_DIR environment variable"