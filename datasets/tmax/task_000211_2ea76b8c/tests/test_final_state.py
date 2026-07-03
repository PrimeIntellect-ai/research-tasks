# test_final_state.py

import os
import stat
import subprocess
import time
import re
from datetime import datetime, timedelta, timezone

def test_directories_and_files():
    """Verify the existence and permissions of required directories and files."""
    assert os.path.isdir("/home/user/capacity_data"), "Directory /home/user/capacity_data does not exist."
    assert os.path.isfile("/home/user/capacity_data/metrics.log"), "File metrics.log does not exist."
    assert os.path.isfile("/home/user/monitor/cap_monitor.cpp"), "File cap_monitor.cpp does not exist."

    executable_path = "/home/user/monitor/cap_monitor"
    assert os.path.isfile(executable_path), "Executable cap_monitor does not exist."
    st = os.stat(executable_path)
    assert bool(st.st_mode & stat.S_IXUSR), "cap_monitor is not executable."

    supervisor_path = "/home/user/monitor/supervise.sh"
    assert os.path.isfile(supervisor_path), "Script supervise.sh does not exist."
    st = os.stat(supervisor_path)
    assert bool(st.st_mode & stat.S_IXUSR), "supervise.sh is not executable."

def test_acls():
    """Verify that the user 'nobody' has explicit read-only access to metrics.log."""
    try:
        output = subprocess.check_output(["getfacl", "/home/user/capacity_data/metrics.log"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run getfacl on metrics.log.")

    acl_found = False
    for line in output.splitlines():
        if re.match(r'^user:nobody:r--', line):
            acl_found = True
            break
    assert acl_found, "ACL rule for user 'nobody' with read-only access (r--) is missing."

def test_supervisor_and_daemon_state():
    """Verify that supervise.sh and cap_monitor are running."""
    try:
        subprocess.check_output(["pgrep", "-f", "supervise.sh"])
    except subprocess.CalledProcessError:
        pytest.fail("supervise.sh is not running.")

    try:
        subprocess.check_output(["pgrep", "-f", "cap_monitor"])
    except subprocess.CalledProcessError:
        pytest.fail("cap_monitor is not running.")

def test_log_formatting_and_routing_data():
    """Verify log contents, format, interface, gateway, and timezone."""
    # Get expected default interface and gateway
    try:
        ip_route_out = subprocess.check_output(["ip", "route"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run 'ip route'.")

    expected_iface = None
    expected_gw = None
    for line in ip_route_out.splitlines():
        if line.startswith("default"):
            parts = line.split()
            if "dev" in parts:
                expected_iface = parts[parts.index("dev") + 1]
            if "via" in parts:
                expected_gw = parts[parts.index("via") + 1]
            break

    assert expected_iface is not None, "Could not determine default interface from 'ip route'."
    assert expected_gw is not None, "Could not determine default gateway from 'ip route'."

    log_file = "/home/user/capacity_data/metrics.log"
    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 3, "metrics.log does not contain at least 3 lines."

    # Check the last line
    last_line = lines[-1].strip()

    # Regex: [YYYY-MM-DD HH:MM:SS] IFACE:<interface_name> GW:<gateway_ip> LOAD:<1-min-load>
    match = re.match(r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] IFACE:([a-zA-Z0-9_-]+) GW:([0-9\.]+) LOAD:([0-9\.]+)$', last_line)
    assert match is not None, f"Log line format is incorrect: {last_line}"

    log_time_str, log_iface, log_gw, log_load = match.groups()

    assert log_iface == expected_iface, f"Logged interface '{log_iface}' does not match expected '{expected_iface}'."
    assert log_gw == expected_gw, f"Logged gateway '{log_gw}' does not match expected '{expected_gw}'."

    # Timezone validation (Asia/Tokyo is UTC+9)
    log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=9)))
    current_time = datetime.now(timezone.utc)

    delta = abs((current_time - log_time).total_seconds())
    assert delta < 10, f"Logged time {log_time_str} (JST) is too far from current time. Delta: {delta}s."

def test_restart_policy():
    """Verify that the supervisor restarts cap_monitor when killed."""
    try:
        # Get current PID
        pid_out = subprocess.check_output(["pgrep", "-f", "cap_monitor"], text=True).strip()
        old_pids = set(pid_out.split())
    except subprocess.CalledProcessError:
        pytest.fail("cap_monitor is not running before restart test.")

    # Kill it
    subprocess.run(["pkill", "-f", "cap_monitor"])

    # Wait for restart
    time.sleep(3)

    try:
        pid_out = subprocess.check_output(["pgrep", "-f", "cap_monitor"], text=True).strip()
        new_pids = set(pid_out.split())
    except subprocess.CalledProcessError:
        pytest.fail("cap_monitor was not restarted by the supervisor.")

    assert new_pids != old_pids, "cap_monitor PID did not change or it wasn't killed successfully."