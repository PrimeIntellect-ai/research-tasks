# test_final_state.py
import os
import json
import math

def test_parsed_metrics_csv():
    raw_log = "/home/user/raw_app.log"
    csv_file = "/home/user/parsed_metrics.csv"

    assert os.path.exists(raw_log), f"{raw_log} is missing."
    assert os.path.exists(csv_file), f"Expected extracted CSV at {csv_file} does not exist."

    expected_lines = []
    with open(raw_log, "r") as f:
        for line in f:
            if "[METRIC]" in line:
                # 2023-10-01T12:00:00Z [METRIC] endpoint=/api/v1/auth latency=123ms status=200 worker=0
                parts = line.strip().split()
                timestamp = parts[0]
                endpoint = parts[2].split("=")[1]
                latency = parts[3].split("=")[1].replace("ms", "")
                status = parts[4].split("=")[1]
                expected_lines.append(f"{timestamp},{endpoint},{latency},{status}")

    with open(csv_file, "r") as f:
        actual_lines = [l.strip() for l in f if l.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, got {len(actual_lines)}."
    assert actual_lines == expected_lines, "CSV contents do not match the expected extraction from raw_app.log."

def test_p90_json_summary():
    csv_file = "/home/user/parsed_metrics.csv"
    json_file = "/home/user/dashboard_summary.json"

    assert os.path.exists(csv_file), f"{csv_file} must exist."
    assert os.path.exists(json_file), f"Expected JSON summary at {json_file} does not exist."

    latencies = {}
    with open(csv_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(",")
            assert len(parts) == 4, f"Invalid CSV format: {line}"
            endpoint = parts[1]
            latency = int(parts[2])
            if endpoint not in latencies:
                latencies[endpoint] = []
            latencies[endpoint].append(latency)

    expected_p90 = {}
    for ep, lats in latencies.items():
        sorted_lats = sorted(lats)
        n = len(sorted_lats)
        # Nearest rank method: 90th percentile
        # index = ceil(0.9 * n) - 1
        idx = math.ceil(0.9 * n) - 1
        expected_p90[ep] = sorted_lats[idx]

    with open(json_file, "r") as f:
        try:
            actual_p90 = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_file} is not valid JSON."

    assert actual_p90 == expected_p90, f"JSON summary P90 values do not match expected. Expected {expected_p90}, got {actual_p90}."

def test_rotating_log_files():
    log_file = "/home/user/dashboard.log"
    assert os.path.exists(log_file), f"Expected log file {log_file} does not exist."

    # Check that at least one rotation happened since max_bytes is 150
    rotated_log = "/home/user/dashboard.log.1"
    assert os.path.exists(rotated_log), f"Expected rotated log file {rotated_log} does not exist. Rotation may not be configured correctly."

    # Read all lines from all log files
    log_files = [f"/home/user/dashboard.log{ext}" for ext in ["", ".1", ".2", ".3"]]
    actual_log_lines = []
    for lf in log_files:
        if os.path.exists(lf):
            with open(lf, "r") as f:
                actual_log_lines.extend([l.strip() for l in f if l.strip()])

    # Recompute expected lines
    json_file = "/home/user/dashboard_summary.json"
    with open(json_file, "r") as f:
        actual_p90 = json.load(f)

    expected_log_lines = []
    for ep in sorted(actual_p90.keys()):
        expected_log_lines.append(f"Endpoint {ep} P90: {actual_p90[ep]}ms")

    # Order in logs might be split across files, but combined they should match the sorted order
    # since the task says "sorted alphabetically by endpoint name"
    assert actual_log_lines == expected_log_lines, f"Log lines across rotated files do not match expected format or order. Expected {expected_log_lines}, got {actual_log_lines}."