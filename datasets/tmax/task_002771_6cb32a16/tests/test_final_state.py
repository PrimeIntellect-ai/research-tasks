# test_final_state.py

import os
import re
import pytest

def compute_truth():
    log_path = '/home/user/system_logs.dat'
    assert os.path.exists(log_path), f"Missing file: {log_path}"

    with open(log_path, 'rb') as f:
        raw_data = f.read()

    sanitized_chars = []
    for b in raw_data:
        if 0x20 <= b <= 0x7E or b == 0x0A or b == 0x0D:
            sanitized_chars.append(chr(b))

    sanitized_text = "".join(sanitized_chars)
    lines = sanitized_text.splitlines()

    total_errors = 0
    first_anomaly_ts = None
    window = []

    for line in lines:
        if not line:
            continue
        is_error = "] ERROR " in line
        if is_error:
            total_errors += 1

        window.append(is_error)
        if len(window) > 100:
            window.pop(0)

        if sum(window) >= 20 and first_anomaly_ts is None:
            m = re.search(r'\[(\d+)\]', line)
            if m:
                first_anomaly_ts = m.group(1)

    if first_anomaly_ts is None:
        first_anomaly_ts = "NONE"

    return str(first_anomaly_ts), str(total_errors)

def test_anomaly_report_generated_and_correct():
    report_path = "/home/user/anomaly_report.txt"
    assert os.path.exists(report_path), f"Missing file: {report_path}. Did you run the C program?"

    expected_ts, expected_errors = compute_truth()

    with open(report_path, 'r') as f:
        content = f.read()

    assert f"First Anomaly Detected At: {expected_ts}" in content, (
        f"Expected to find 'First Anomaly Detected At: {expected_ts}' in {report_path}. "
        "Check your sliding window logic and sanitization."
    )

    assert f"Total Errors Logged: {expected_errors}" in content, (
        f"Expected to find 'Total Errors Logged: {expected_errors}' in {report_path}. "
        "Check your error counting logic."
    )