# test_final_state.py

import os
import json
import glob
import pytest

def test_analyze_c_source_exists_and_uses_mmap():
    source_path = "/home/user/analyze.c"
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."

    with open(source_path, "r") as f:
        content = f.read()

    assert "mmap" in content, f"Source file {source_path} does not seem to use 'mmap' as required."

def test_analyze_binary_exists_and_executable():
    binary_path = "/home/user/analyze"
    assert os.path.isfile(binary_path), f"Executable {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

    with open(binary_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {binary_path} is not an ELF binary."

def test_alerts_log_content():
    json_path = "/home/user/thresholds.json"
    logs_dir = "/home/user/logs"
    alerts_path = "/home/user/alerts.log"

    assert os.path.isfile(json_path), f"Missing {json_path}"
    with open(json_path, "r") as f:
        thresholds = json.load(f)

    log_files = sorted(glob.glob(os.path.join(logs_dir, "*.csv")))

    expected_alerts = []
    for log_file in log_files:
        with open(log_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 3:
                    timestamp, mount_point, usage_str = parts
                    try:
                        usage_mb = int(usage_str)
                    except ValueError:
                        continue

                    if mount_point in thresholds:
                        limit_mb = thresholds[mount_point]
                        if usage_mb > limit_mb:
                            expected_alerts.append(
                                f"[{timestamp}] ALERT: {mount_point} exceeded threshold "
                                f"(Current: {usage_mb} MB, Limit: {limit_mb} MB)"
                            )

    assert os.path.isfile(alerts_path), f"Output file {alerts_path} does not exist."

    with open(alerts_path, "r") as f:
        actual_alerts = [line.strip() for line in f if line.strip()]

    assert actual_alerts == expected_alerts, (
        f"Contents of {alerts_path} do not match the expected alerts.\n"
        f"Expected:\n{chr(10).join(expected_alerts)}\n"
        f"Actual:\n{chr(10).join(actual_alerts)}"
    )