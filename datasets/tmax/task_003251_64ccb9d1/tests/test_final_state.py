# test_final_state.py

import os
import re
import datetime

def test_cpp_file_exists():
    path = "/home/user/net_monitor.cpp"
    assert os.path.isfile(path), f"The C++ source file {path} does not exist."

def test_executable_exists_and_executable():
    path = "/home/user/net_monitor"
    assert os.path.isfile(path), f"The executable {path} does not exist."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_log_file_format_and_values():
    log_path = "/home/user/network_log.txt"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    # Check format exactly
    pattern = r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] RX: (\d+) TX: (\d+)$'
    match = re.match(pattern, content)
    assert match is not None, f"The content of {log_path} does not match the exact format required. Got: {content}"

    timestamp_str, rx_str, tx_str = match.groups()

    # Check that traffic was generated (RX and TX > 0)
    rx = int(rx_str)
    tx = int(tx_str)
    assert rx > 0, f"RX bytes must be strictly greater than 0, but got {rx}. Local traffic simulation may have failed."
    assert tx > 0, f"TX bytes must be strictly greater than 0, but got {tx}. Local traffic simulation may have failed."

    # Validate timezone (Asia/Tokyo is UTC+9)
    log_time = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    log_time = log_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))

    mtime = os.path.getmtime(log_path)
    file_time = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc)

    # Allow a small difference (e.g., 60 seconds) between file creation and logged time
    diff = abs((log_time - file_time).total_seconds())
    assert diff <= 60, (
        f"Logged time '{timestamp_str}' does not match the file's modification time in Asia/Tokyo. "
        f"File modified at {file_time.strftime('%Y-%m-%d %H:%M:%S')} UTC."
    )