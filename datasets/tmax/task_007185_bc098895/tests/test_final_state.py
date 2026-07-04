# test_final_state.py

import os
import json
import gzip
import struct
import pytest

SUMMARY_FILE = "/home/user/config_summary.json"
BASE_DIR = "/home/user/config_backups"

def parse_ccf_stream(f):
    try:
        header = f.read(10)
        if len(header) < 10:
            return None
        magic, timestamp, entry_count = struct.unpack("<4s I H", header)
        if magic != b"CCF1":
            return None

        target_version = None
        for _ in range(entry_count):
            key_len_data = f.read(2)
            if len(key_len_data) < 2:
                break
            key_len = struct.unpack("<H", key_len_data)[0]
            key = f.read(key_len).decode('utf-8', errors='replace')

            val_len_data = f.read(4)
            if len(val_len_data) < 4:
                break
            val_len = struct.unpack("<I", val_len_data)[0]
            val = f.read(val_len).decode('utf-8', errors='replace')

            if key == "target_version":
                target_version = val

        return timestamp, target_version
    except (struct.error, OSError, EOFError):
        return None

def compute_expected_summary():
    expected = {}
    if not os.path.exists(BASE_DIR):
        return expected

    for server_name in os.listdir(BASE_DIR):
        server_dir = os.path.join(BASE_DIR, server_name)
        if not os.path.isdir(server_dir):
            continue

        latest_ts = -1
        latest_version = None

        for filename in os.listdir(server_dir):
            filepath = os.path.join(server_dir, filename)
            if not os.path.isfile(filepath):
                continue

            parsed = None
            if filename.endswith(".ccf.gz"):
                try:
                    with gzip.open(filepath, "rb") as f:
                        parsed = parse_ccf_stream(f)
                except Exception:
                    continue
            elif filename.endswith(".ccf"):
                try:
                    with open(filepath, "rb") as f:
                        parsed = parse_ccf_stream(f)
                except Exception:
                    continue

            if parsed:
                ts, version = parsed
                if version is not None and ts > latest_ts:
                    latest_ts = ts
                    latest_version = version

        if latest_version is not None:
            expected[server_name] = {
                "latest_timestamp": latest_ts,
                "target_version": latest_version
            }

    return expected

def test_summary_file_exists():
    assert os.path.exists(SUMMARY_FILE), f"The summary file {SUMMARY_FILE} does not exist."
    assert os.path.isfile(SUMMARY_FILE), f"The path {SUMMARY_FILE} is not a file."

def test_summary_file_content():
    assert os.path.exists(SUMMARY_FILE), f"The summary file {SUMMARY_FILE} does not exist."

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {SUMMARY_FILE} as JSON: {e}")

    expected_data = compute_expected_summary()

    assert isinstance(actual_data, dict), "The JSON root must be an object (dictionary)."

    # Check servers
    missing_servers = set(expected_data.keys()) - set(actual_data.keys())
    assert not missing_servers, f"Missing servers in summary: {missing_servers}"

    extra_servers = set(actual_data.keys()) - set(expected_data.keys())
    assert not extra_servers, f"Unexpected servers in summary: {extra_servers}"

    # Check content
    for server, expected_info in expected_data.items():
        actual_info = actual_data[server]
        assert isinstance(actual_info, dict), f"Value for {server} must be an object."

        assert "latest_timestamp" in actual_info, f"Missing 'latest_timestamp' for {server}"
        assert "target_version" in actual_info, f"Missing 'target_version' for {server}"

        assert actual_info["latest_timestamp"] == expected_info["latest_timestamp"], \
            f"Incorrect latest_timestamp for {server}. Expected {expected_info['latest_timestamp']}, got {actual_info['latest_timestamp']}."

        assert actual_info["target_version"] == expected_info["target_version"], \
            f"Incorrect target_version for {server}. Expected {expected_info['target_version']}, got {actual_info['target_version']}."