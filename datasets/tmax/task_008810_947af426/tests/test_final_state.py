# test_final_state.py

import os
import re
import pytest

LOGICAL_CLUSTER_DIR = "/home/user/logical_cluster"
RAW_STORAGE_DIR = "/home/user/raw_storage"
CONF_FILE = "/home/user/capacity.conf"
DAEMON_SCRIPT = "/home/user/capacity-daemon.sh"
INIT_SCRIPT = "/home/user/cluster-init.sh"
PID_FILE = "/home/user/daemon.pid"
ALERT_LOG = "/home/user/capacity_alerts.log"

def test_logical_cluster_symlinks():
    assert os.path.isdir(LOGICAL_CLUSTER_DIR), f"Directory {LOGICAL_CLUSTER_DIR} does not exist."

    expected_links = {
        "vol1": "node_alpha",
        "vol2": "node_beta",
        "vol3": "node_gamma",
        "vol4": "node_delta",
    }

    for link_name, target_node in expected_links.items():
        link_path = os.path.join(LOGICAL_CLUSTER_DIR, link_name)
        assert os.path.islink(link_path), f"{link_path} is not a symlink."

        target_path = os.readlink(link_path)
        # Check if it points to the correct node (absolute or relative)
        expected_abs_target = os.path.join(RAW_STORAGE_DIR, target_node)
        actual_abs_target = os.path.normpath(os.path.join(LOGICAL_CLUSTER_DIR, target_path))

        assert actual_abs_target == expected_abs_target, f"Symlink {link_name} points to {actual_abs_target}, expected {expected_abs_target}."

def test_capacity_conf():
    assert os.path.isfile(CONF_FILE), f"Config file {CONF_FILE} does not exist."
    with open(CONF_FILE, "r") as f:
        content = f.read()

    assert "THRESHOLD_BYTES=15000000" in content, f"{CONF_FILE} missing THRESHOLD_BYTES=15000000"
    assert "ALERT_LOG=/home/user/capacity_alerts.log" in content, f"{CONF_FILE} missing ALERT_LOG=/home/user/capacity_alerts.log"

def test_scripts_executable():
    assert os.path.isfile(DAEMON_SCRIPT), f"{DAEMON_SCRIPT} does not exist."
    assert os.access(DAEMON_SCRIPT, os.X_OK), f"{DAEMON_SCRIPT} is not executable."

    assert os.path.isfile(INIT_SCRIPT), f"{INIT_SCRIPT} does not exist."
    assert os.access(INIT_SCRIPT, os.X_OK), f"{INIT_SCRIPT} is not executable."

def test_daemon_running():
    assert os.path.isfile(PID_FILE), f"PID file {PID_FILE} does not exist."
    with open(PID_FILE, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {PID_FILE} does not contain a valid integer PID."
    pid = int(pid_str)

    # Check if process exists
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

    # Check if it's our bash script (optional but good)
    cmdline_file = f"/proc/{pid}/cmdline"
    if os.path.isfile(cmdline_file):
        with open(cmdline_file, "r") as f:
            cmdline = f.read().replace('\0', ' ')
        assert "capacity-daemon.sh" in cmdline or "bash" in cmdline, f"Process {pid} does not seem to be the capacity daemon."

def test_alert_log():
    assert os.path.isfile(ALERT_LOG), f"Alert log {ALERT_LOG} does not exist. Daemon may not have run or logic is incorrect."

    with open(ALERT_LOG, "r") as f:
        content = f.read()

    assert "CRITICAL: Usage at " in content, f"Alert log does not contain 'CRITICAL: Usage at '."

    # Find all matches
    matches = re.findall(r"CRITICAL: Usage at (\d+) bytes", content)
    assert len(matches) > 0, "No correctly formatted alert lines found in the log."

    for match in matches:
        bytes_val = int(match)
        assert bytes_val > 15000000, f"Logged bytes {bytes_val} is not greater than the threshold 15000000."