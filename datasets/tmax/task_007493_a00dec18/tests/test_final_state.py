# test_final_state.py

import os
import re
import pytest

def test_systemd_unit_file():
    """Verify the systemd unit file is correctly configured."""
    unit_file = "/home/user/systemd/user/monitor.service"
    assert os.path.isfile(unit_file), f"Systemd unit file {unit_file} does not exist."

    with open(unit_file, "r") as f:
        content = f.read()

    # Check Type=oneshot
    assert re.search(r"^Type\s*=\s*oneshot", content, re.MULTILINE | re.IGNORECASE), \
        f"{unit_file} is missing 'Type=oneshot'."

    # Check After=target-server.service
    assert re.search(r"^After\s*=.*target-server\.service", content, re.MULTILINE | re.IGNORECASE), \
        f"{unit_file} is missing 'After=target-server.service'."

    # Check Environment for TZ=Asia/Tokyo
    assert re.search(r"^Environment\s*=.*TZ=Asia/Tokyo", content, re.MULTILINE | re.IGNORECASE), \
        f"{unit_file} is missing 'Environment=TZ=Asia/Tokyo' (or similar)."

def test_c_source_and_binary():
    """Verify the C source file and compiled binary exist."""
    c_source = "/home/user/monitor.c"
    binary = "/home/user/monitor"

    assert os.path.isfile(c_source), f"C source file {c_source} does not exist."
    assert os.path.isfile(binary), f"Compiled binary {binary} does not exist."
    assert os.access(binary, os.X_OK), f"Compiled binary {binary} is not executable."

def test_monitor_log():
    """Verify the monitor.log file contains a successful check entry."""
    log_file = "/home/user/monitor.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    # Look for OK: YYYY-MM-DD HH:MM:SS
    pattern = r"^OK:\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"
    assert re.search(pattern, content, re.MULTILINE), \
        f"{log_file} does not contain a successful 'OK: YYYY-MM-DD HH:MM:SS' entry."