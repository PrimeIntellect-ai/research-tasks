# test_final_state.py

import os
import re
from datetime import datetime, timezone, timedelta
import pytest

def get_expected_fstab_count():
    if not os.path.exists("/etc/fstab"):
        return 0
    with open("/etc/fstab", "r") as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            count += 1
    return count

def test_monitoring_log_exists():
    log_path = "/home/user/monitoring_logs/uptime.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the hook run and create it?"

def test_monitoring_log_format_and_content():
    log_path = "/home/user/monitoring_logs/uptime.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"Log file {log_path} is empty."

    last_line = lines[-1].strip()

    # Regex to match: [YYYY-MM-DD HH:MM:SS UTC] FSTAB_ENTRIES: <count>
    pattern = r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) UTC\] FSTAB_ENTRIES: (\d+)$"
    match = re.match(pattern, last_line)

    assert match is not None, f"Last line in log does not match expected format: '{last_line}'"

    time_str, count_str = match.groups()

    # Check count
    expected_count = get_expected_fstab_count()
    assert int(count_str) == expected_count, f"Expected {expected_count} FSTAB_ENTRIES, but found {count_str}."

    # Check time (should be close to current UTC time)
    log_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    current_time = datetime.now(timezone.utc)

    time_diff = abs((current_time - log_time).total_seconds())
    assert time_diff < 3600, f"Logged time {time_str} is not close to current UTC time. Make sure TZ=UTC was used."

def test_post_commit_hook_executable():
    hook_path = "/home/user/monitor_src/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."