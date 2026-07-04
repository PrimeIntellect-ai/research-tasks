# test_final_state.py

import os
import re
import subprocess
import pytest

EXECUTABLE = "/home/user/sre_monitor"
LOG_FILE = "/home/user/system_status.log"
FSTAB_FILE = "/home/user/sys_config/fstab"
ROUTES_FILE = "/home/user/sys_config/routes"

def test_executable_exists_and_runnable():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} does not exist."
    assert os.access(EXECUTABLE, os.X_OK), f"{EXECUTABLE} is not executable."

def test_log_file_generated_and_format_correct():
    # Run the executable to generate the log file
    result = subprocess.run([EXECUTABLE], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {EXECUTABLE} failed with error: {result.stderr}"

    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not generated."

    with open(LOG_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, "Log file does not contain enough lines."

    # Line 1: Time
    time_match = re.match(r"^Time:\s+\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST$", lines[0])
    assert time_match, f"Time line format is incorrect: {lines[0]}"

    # Line 2: Gateway
    assert lines[1] == "Gateway: 10.0.2.1", f"Gateway line is incorrect: {lines[1]}"

    # Line 3: EXT4 Mounts
    mounts_line = lines[2].replace(" ", "")
    assert mounts_line == "EXT4Mounts:/,/var/log", f"EXT4 Mounts line is incorrect: {lines[2]}"

def test_no_hardcoding():
    # Replace contents to test parsing logic
    original_fstab = ""
    original_routes = ""

    with open(FSTAB_FILE, 'r') as f:
        original_fstab = f.read()
    with open(ROUTES_FILE, 'r') as f:
        original_routes = f.read()

    new_fstab = """# /etc/fstab
UUID=abc /new_root ext4 defaults 0 1
UUID=def /data ext4 defaults 0 2
UUID=ghi /swap swap sw 0 0
"""
    new_routes = """Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
"""

    try:
        with open(FSTAB_FILE, 'w') as f:
            f.write(new_fstab)
        with open(ROUTES_FILE, 'w') as f:
            f.write(new_routes)

        result = subprocess.run([EXECUTABLE], capture_output=True, text=True)
        assert result.returncode == 0, "Executable failed with modified config files."

        with open(LOG_FILE, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        assert len(lines) >= 3, "Log file does not contain enough lines after modifying configs."
        assert lines[1] == "Gateway: 192.168.1.1", f"Gateway line is hardcoded or incorrectly parsed: {lines[1]}"

        mounts_line = lines[2].replace(" ", "")
        assert mounts_line == "EXT4Mounts:/new_root,/data", f"EXT4 Mounts line is hardcoded or incorrectly parsed: {lines[2]}"

    finally:
        # Restore original files
        with open(FSTAB_FILE, 'w') as f:
            f.write(original_fstab)
        with open(ROUTES_FILE, 'w') as f:
            f.write(original_routes)