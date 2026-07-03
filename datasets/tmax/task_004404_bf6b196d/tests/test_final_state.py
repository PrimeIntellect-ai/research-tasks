# test_final_state.py

import os
import re
import pytest

def compute_expected_anomaly():
    telemetry_path = "/home/user/telemetry.jsonl"
    if not os.path.exists(telemetry_path):
        return None, None

    bucket_counts = {}

    with open(telemetry_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if '"status": "failed"' in line:
                continue
            if '"action": "edit"' in line:
                match = re.search(r'"timestamp"\s*:\s*(\d+)', line)
                if match:
                    ts = int(match.group(1))
                    bucket_id = ts // 3600
                    bucket_counts[bucket_id] = bucket_counts.get(bucket_id, 0) + 1

    sorted_buckets = sorted(bucket_counts.keys())

    sum_edits = 0
    count_buckets = 0

    for bucket in sorted_buckets:
        edits = bucket_counts[bucket]
        if count_buckets >= 5:
            mean = sum_edits / count_buckets
            if edits > 3.0 * mean:
                return bucket * 3600, edits

        sum_edits += edits
        count_buckets += 1

    return None, None

def test_c_source_exists():
    """Test that the C source code file exists."""
    c_file = "/home/user/detect_anomaly.c"
    assert os.path.exists(c_file), f"Missing C source file: {c_file}"

def test_anomaly_report_exists_and_correct():
    """Test that the anomaly_report.txt file exists and contains the correct output."""
    report_file = "/home/user/anomaly_report.txt"
    assert os.path.exists(report_file), f"Missing anomaly report file: {report_file}"

    expected_hour, expected_count = compute_expected_anomaly()
    assert expected_hour is not None, "Could not find an anomaly in the telemetry data."

    expected_text = f"ANOMALY_HOUR: {expected_hour}, COUNT: {expected_count}"

    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == expected_text, f"Report content is incorrect. Expected '{expected_text}', got '{content}'"