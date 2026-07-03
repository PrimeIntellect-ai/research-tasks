# test_final_state.py
import os
import struct
from datetime import datetime, timezone

def test_archive_log_script_exists():
    path = "/home/user/archive_log.py"
    assert os.path.isfile(path), f"File {path} does not exist. You must create the python script."

def test_sanitized_log_content():
    path = "/home/user/sanitized.log"
    assert os.path.isfile(path), f"File {path} does not exist. The script must create it."

    expected_content = (
        "2023-10-15 08:23:45 [REDACTED] User login successful\n"
        "2023-10-15 08:24:10 [REDACTED] Database connection established\n"
        "2023-10-15 08:25:00 [REDACTED] Timeout error\n"
    )

    with open(path, "r") as f:
        content = f.read()

    assert content == expected_content, f"Content of {path} does not match the expected redacted output."

def test_index_bin_content():
    path = "/home/user/index.bin"
    assert os.path.isfile(path), f"File {path} does not exist. The script must create it."

    # Recompute expected binary data
    lines = [
        ("2023-10-15 08:23:45", "2023-10-15 08:23:45 [REDACTED] User login successful\n"),
        ("2023-10-15 08:24:10", "2023-10-15 08:24:10 [REDACTED] Database connection established\n"),
        ("2023-10-15 08:25:00", "2023-10-15 08:25:00 [REDACTED] Timeout error\n"),
    ]

    expected_binary = b""
    current_offset = 0
    for ts_str, line in lines:
        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        ts = int(dt.timestamp())
        expected_binary += struct.pack("<QQ", ts, current_offset)
        current_offset += len(line.encode('utf-8'))

    with open(path, "rb") as f:
        binary_content = f.read()

    assert binary_content == expected_binary, f"Content of {path} does not match the expected binary index."