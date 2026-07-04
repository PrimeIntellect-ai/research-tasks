# test_final_state.py

import os
import json
import pytest

def test_unified_jsonl_exists_and_correct():
    file_path = "/home/user/output/unified.jsonl"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    expected_records = [
        {"timestamp": "2023-10-01T10:00:00Z", "normalized_msg": "db connection timeout", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:01:00Z", "normalized_msg": "db connection timeout", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:02:00Z", "normalized_msg": "db connection timeout", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:05:00Z", "normalized_msg": "disk space low on var", "severity": "MEDIUM"},
        {"timestamp": "2023-10-01T10:08:00Z", "normalized_msg": "db connection timeout", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:09:00Z", "normalized_msg": "db connection timeout", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:12:00Z", "normalized_msg": "memory leak detected in caching layer", "severity": "CRITICAL"},
        {"timestamp": "2023-10-01T10:15:00Z", "normalized_msg": "cpu usage at 99", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:16:00Z", "normalized_msg": "cpu usage at 99 percent", "severity": "HIGH"},
        {"timestamp": "2023-10-01T10:18:00Z", "normalized_msg": "network partition detected", "severity": "CRITICAL"},
        {"timestamp": "2023-10-01T10:20:00Z", "normalized_msg": "completely unrelated error", "severity": "UNKNOWN"}
    ]

    actual_records = []
    with open(file_path, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {file_path} is not valid JSON: {line}")

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records in {file_path}, but found {len(actual_records)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, (
            f"Record at line {i+1} does not match expected.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

def test_anomalies_txt_exists_and_correct():
    file_path = "/home/user/output/anomalies.txt"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_anomalies = ["db connection timeout"]

    assert len(lines) == len(expected_anomalies), (
        f"Expected {len(expected_anomalies)} anomalies in {file_path}, but found {len(lines)}."
    )

    for i, (actual, expected) in enumerate(zip(lines, expected_anomalies)):
        assert actual == expected, (
            f"Anomaly at line {i+1} does not match expected.\n"
            f"Expected: '{expected}'\n"
            f"Actual:   '{actual}'"
        )