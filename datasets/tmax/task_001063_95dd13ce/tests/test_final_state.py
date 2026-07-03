# test_final_state.py
import os
import subprocess
import pytest

def test_monitor_log_content():
    log_path = "/home/user/app/monitor.log"
    assert os.path.exists(log_path), f"File {log_path} is missing. The monitor service may not have completed successfully."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "STATUS: ALL_SYSTEMS_GO"
    assert content == expected, f"Incorrect content in {log_path}. Expected '{expected}', got '{content}'"

def test_ssh_tunnel_running():
    try:
        output = subprocess.check_output(["ps", "x", "-o", "command"]).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to check processes: {e}")

    ssh_found = False
    for line in output.splitlines():
        if line.startswith("ssh ") or "/ssh " in line or "ssh" in line.split()[0]:
            if "9000" in line and "8002" in line:
                ssh_found = True
                break

    assert ssh_found, "SSH tunnel process (forwarding port 9000 to 8002) is not running."