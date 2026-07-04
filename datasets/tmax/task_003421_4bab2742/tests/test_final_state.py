# test_final_state.py

import os
import re
import subprocess
import pytest

LOG_DIR = "/home/user/logs"
SCRIPT_PATH = "/home/user/net_monitor.py"
LATEST_LINK = "/home/user/logs/latest.log"
PORTS_FILE = "/home/user/ports.txt"

def test_script_and_dir_exist():
    assert os.path.isdir(LOG_DIR), f"Directory {LOG_DIR} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_crontab_entry():
    try:
        output = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("No crontab found for the current user.")

    # Check for the required crontab entry
    match = re.search(r'^\s*\*\s+\*\s+\*\s+\*\s+\*.*python3\s+/home/user/net_monitor\.py', output, re.MULTILINE)
    assert match is not None, "Crontab entry for net_monitor.py every minute is missing or incorrect."

def test_symlink_latest_log():
    assert os.path.islink(LATEST_LINK), f"{LATEST_LINK} is not a symbolic link."

    target = os.readlink(LATEST_LINK)
    # Must be a relative link
    assert not os.path.isabs(target), f"Symlink target '{target}' is not a relative link."

    # Target must match run_<TIMESTAMP>.log
    assert re.match(r'^run_\d+\.log$', target), f"Symlink target '{target}' does not match the required naming format."

    # Target must exist
    target_path = os.path.join(LOG_DIR, target)
    assert os.path.isfile(target_path), f"Symlink target file {target_path} does not exist."

def test_latest_log_content():
    assert os.path.exists(LATEST_LINK), f"{LATEST_LINK} does not exist."

    with open(LATEST_LINK, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "PORT 8000: DOWN",
        "PORT 8001: UP",
        "PORT 8002: DOWN"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in latest.log, found {len(content)}."
    for expected, actual in zip(expected_lines, content):
        assert expected == actual.strip(), f"Expected line '{expected}', found '{actual.strip()}'."

def test_log_rotation_and_file_count():
    assert os.path.isdir(LOG_DIR), f"Directory {LOG_DIR} does not exist."

    log_files = []
    for f in os.listdir(LOG_DIR):
        full_path = os.path.join(LOG_DIR, f)
        if os.path.isfile(full_path) and not os.path.islink(full_path) and f.startswith("run_") and f.endswith(".log"):
            log_files.append(full_path)

    num_files = len(log_files)
    assert num_files >= 1, "No log files found in the log directory."
    assert num_files <= 3, f"Expected at most 3 log files due to rotation, but found {num_files}. Log rotation may not be working correctly."