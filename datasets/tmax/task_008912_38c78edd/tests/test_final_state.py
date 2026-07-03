# test_final_state.py

import os
import math
import pytest

def get_expected_results():
    access_log = "/home/user/access.log"
    if not os.path.exists(access_log):
        return 0, []

    with open(access_log, "r") as f:
        lines = f.readlines()

    api_lines = [line for line in lines if "/api/v1/process" in line]

    error_times = []
    for line in api_lines:
        parts = line.split()
        if len(parts) >= 2:
            status = parts[-3]
            if status in ("500", "502"):
                try:
                    error_times.append(float(parts[-1]))
                except ValueError:
                    pass

    count = len(error_times)
    if count == 0:
        return 0, []

    mean = sum(error_times) / count
    var = sum((x - mean) ** 2 for x in error_times) / count
    stddev = math.sqrt(var)
    threshold = mean + 2 * stddev

    expected_anomalies = []
    for line in api_lines:
        parts = line.split()
        try:
            val = float(parts[-1])
            if val > threshold:
                expected_anomalies.append(line.strip())
        except ValueError:
            pass

    return count, expected_anomalies

def test_debug_counts_file():
    """Verify that debug_counts.txt contains the correct filtered 5xx error count."""
    debug_file = "/home/user/debug_counts.txt"
    assert os.path.exists(debug_file), f"Missing file: {debug_file}. The script must create this file."

    expected_count, _ = get_expected_results()
    expected_text = f"Filtered 5xx error count: {expected_count}"

    with open(debug_file, "r") as f:
        content = f.read().strip()

    assert content == expected_text, f"Incorrect content in {debug_file}. Expected '{expected_text}', got '{content}'."

def test_anomalies_file():
    """Verify that anomalies.log contains the correct anomalous log lines."""
    anomalies_file = "/home/user/anomalies.log"
    assert os.path.exists(anomalies_file), f"Missing file: {anomalies_file}. The script must create this file."

    _, expected_anomalies = get_expected_results()

    with open(anomalies_file, "r") as f:
        actual_anomalies = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_anomalies == expected_anomalies, (
        f"Incorrect anomalies recorded. Expected {len(expected_anomalies)} lines, "
        f"found {len(actual_anomalies)}. Check your filtering and variance calculation."
    )

def test_script_is_executable():
    """Verify that analyze_logs.sh is executable."""
    script_file = "/home/user/analyze_logs.sh"
    assert os.path.exists(script_file), f"Missing file: {script_file}"
    assert os.access(script_file, os.X_OK), f"File is not executable: {script_file}"