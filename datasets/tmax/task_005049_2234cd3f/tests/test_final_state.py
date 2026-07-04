# test_final_state.py

import os
import json
import pytest

def test_final_metrics_exists():
    file_path = "/home/user/uptime_monitor/final_metrics.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run the script and generate the output?"

def test_final_metrics_values():
    log_path = "/home/user/uptime_monitor/health_logs.txt"
    json_path = "/home/user/uptime_monitor/final_metrics.json"

    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(json_path), f"Output file {json_path} is missing."

    # Compute truth from the actual log file
    total_requests = 0
    error_requests = 0

    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 3:
                continue

            total_requests += 1
            status_str = parts[2]

            if status_str == "TIMEOUT":
                error_requests += 1
            else:
                try:
                    status_code = int(status_str)
                    if status_code >= 500:
                        error_requests += 1
                except ValueError:
                    pass

    expected_uptime_pct = round((1 - (error_requests / total_requests)) * 100, 4) if total_requests > 0 else 0.0
    expected_burn_rate = round((error_requests / total_requests) / 0.001, 4) if total_requests > 0 else 0.0

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "total_requests" in data, "Key 'total_requests' is missing from the JSON output."
    assert data["total_requests"] == total_requests, \
        f"Expected total_requests to be {total_requests}, but got {data['total_requests']}."

    assert "error_requests" in data, "Key 'error_requests' is missing from the JSON output."
    assert data["error_requests"] == error_requests, \
        f"Expected error_requests to be {error_requests} (only 5xx and TIMEOUT count), but got {data['error_requests']}."

    assert "uptime_percentage" in data, "Key 'uptime_percentage' is missing from the JSON output."
    assert data["uptime_percentage"] == expected_uptime_pct, \
        f"Expected uptime_percentage to be {expected_uptime_pct}, but got {data['uptime_percentage']}."

    assert "burn_rate" in data, "Key 'burn_rate' is missing from the JSON output."
    assert data["burn_rate"] == expected_burn_rate, \
        f"Expected burn_rate to be {expected_burn_rate}, but got {data['burn_rate']}."