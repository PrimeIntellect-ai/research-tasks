# test_final_state.py
import os
import json
import stat
import pytest

REPORT_PATH = "/home/user/setup_report.json"
DB_PATH = "/home/user/user_db.txt"
ROUTING_SCRIPT_PATH = "/home/user/user_routing.sh"

def test_setup_report_json():
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON.")

    assert "username" in data, "Missing 'username' in report."
    assert "uid" in data, "Missing 'uid' in report."
    assert "assigned_ip" in data, "Missing 'assigned_ip' in report."
    assert "quota_mb" in data, "Missing 'quota_mb' in report."
    assert "quota_daemon_pid" in data, "Missing 'quota_daemon_pid' in report."

    assert data["username"] == "dev_intern", "Username in report should be 'dev_intern'."
    assert data["assigned_ip"] == "10.0.0.50", "Assigned IP in report should be '10.0.0.50'."
    assert data["quota_mb"] == 500, "Quota MB in report should be 500."

def test_uid_matches_db():
    assert os.path.isfile(DB_PATH), f"{DB_PATH} does not exist. Was the CLI tool run successfully?"

    with open(DB_PATH, "r") as f:
        lines = f.read().strip().split('\n')

    dev_intern_lines = [line for line in lines if line.startswith("dev_intern:")]
    assert len(dev_intern_lines) > 0, "No entry for 'dev_intern' found in user_db.txt."

    # Format: username:password:sandbox:quota:uid
    last_entry = dev_intern_lines[-1]
    parts = last_entry.split(":")
    assert len(parts) == 5, "Invalid format in user_db.txt."
    db_uid = int(parts[4])

    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert data["uid"] == db_uid, f"UID in report ({data['uid']}) does not match UID in DB ({db_uid})."

def test_routing_script():
    assert os.path.isfile(ROUTING_SCRIPT_PATH), f"{ROUTING_SCRIPT_PATH} does not exist."

    # Check executable permission
    st = os.stat(ROUTING_SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{ROUTING_SCRIPT_PATH} is not executable."

    with open(ROUTING_SCRIPT_PATH, "r") as f:
        content = f.read()

    expected_command = "ip route add 10.0.0.50 dev dev_intern_veth"
    assert expected_command in content, f"Expected command '{expected_command}' not found in {ROUTING_SCRIPT_PATH}."

def test_daemon_running_and_pid():
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} does not exist."
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    pid = data.get("quota_daemon_pid")
    assert pid is not None, "quota_daemon_pid is missing in report."
    assert isinstance(pid, int), "quota_daemon_pid must be an integer."

    cmdline_path = f"/proc/{pid}/cmdline"
    assert os.path.isfile(cmdline_path), f"Process with PID {pid} is not running."

    with open(cmdline_path, "r") as f:
        cmdline = f.read().replace('\x00', ' ')

    assert "quota_daemon.py" in cmdline, f"Process {pid} does not appear to be quota_daemon.py. Cmdline: {cmdline}"