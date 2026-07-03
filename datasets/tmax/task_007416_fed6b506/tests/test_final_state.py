# test_final_state.py

import os
import json
import stat
import socket
import re
import pytest

NETMON_DIR = "/home/user/netmon"

def test_files_exist():
    """Verify all required files exist."""
    expected_files = [
        "targets.txt",
        "routing.json",
        "fallback_route.sh",
        "monitor.py",
        "connectivity.log",
        "cron_backup.txt"
    ]
    for filename in expected_files:
        path = os.path.join(NETMON_DIR, filename)
        assert os.path.exists(path), f"File {path} is missing."

def test_ports_listening():
    """Verify that ports 8080 and 8081 are listening."""
    for port in [8080, 8081]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Port {port} is not listening."

def test_routing_json_content():
    """Verify the contents of routing.json."""
    routing_path = os.path.join(NETMON_DIR, "routing.json")
    with open(routing_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("routing.json is not valid JSON.")

    expected_data = {
        "127.0.0.1:8080": {"status": "UP", "priority": 1},
        "127.0.0.1:8081": {"status": "UP", "priority": 2},
        "127.0.0.1:9999": {"status": "DOWN", "priority": 3}
    }

    assert data == expected_data, f"routing.json content does not match expected. Got: {data}"

def test_connectivity_log_content():
    """Verify the contents of connectivity.log."""
    log_path = os.path.join(NETMON_DIR, "connectivity.log")
    with open(log_path, 'r') as f:
        content = f.read()

    assert "Target 127.0.0.1:8080 -> UP" in content, "Missing or incorrect log entry for 8080."
    assert "Target 127.0.0.1:8081 -> UP" in content, "Missing or incorrect log entry for 8081."
    assert "Target 127.0.0.1:9999 -> DOWN" in content, "Missing or incorrect log entry for 9999."

def test_fallback_route_permissions():
    """Verify that fallback_route.sh has 700 permissions."""
    script_path = os.path.join(NETMON_DIR, "fallback_route.sh")
    st = os.stat(script_path)
    perms = oct(st.st_mode)[-3:]
    assert perms == '700', f"fallback_route.sh permissions should be 700, but got {perms}."

def test_cron_backup_content():
    """Verify that the cron backup file contains the correct cron expression."""
    cron_path = os.path.join(NETMON_DIR, "cron_backup.txt")
    with open(cron_path, 'r') as f:
        content = f.read()

    # Check for every 5 minutes cron expression
    # Matches */5 * * * * or 0,5,10... * * * *
    cron_pattern = r'(?:\*/5|(?:[0-9]+,)*[0-9]+)\s+\*\s+\*\s+\*\s+\*.*monitor\.py'
    assert re.search(cron_pattern, content), "Cron backup does not contain the correct 5-minute schedule for monitor.py."