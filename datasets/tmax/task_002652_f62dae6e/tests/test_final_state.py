# test_final_state.py

import os
import re
import requests

def compute_expected_stats(log_path):
    valid_latencies = []
    latest_by_level = {}

    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: 2023-10-25T09:00:00Z | INFO | latency=50ms | Bootup
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                level = parts[1]
                latency_str = parts[2]

                match = re.match(r'^latency=(-?\d+)ms$', latency_str)
                if match:
                    latency_val = int(match.group(1))
                    if latency_val >= 0:
                        valid_latencies.append(latency_val)
                        latest_by_level[level] = line

    if len(valid_latencies) >= 3:
        rolling_avg_3 = sum(valid_latencies[-3:]) / 3.0
    elif len(valid_latencies) > 0:
        rolling_avg_3 = sum(valid_latencies) / float(len(valid_latencies))
    else:
        rolling_avg_3 = 0.0

    return {
        "rolling_avg_3": rolling_avg_3,
        "latest_by_level": latest_by_level
    }

def test_api_stats_endpoint():
    log_path = "/app/logs/events.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    expected_data = compute_expected_stats(log_path)

    try:
        response = requests.get("http://127.0.0.1:8000/api/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the API via Nginx proxy at http://127.0.0.1:8000/api/stats: {e}"

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert "rolling_avg_3" in data, "Missing 'rolling_avg_3' in JSON response."
    assert "latest_by_level" in data, "Missing 'latest_by_level' in JSON response."

    assert abs(data["rolling_avg_3"] - expected_data["rolling_avg_3"]) < 1e-5, \
        f"Expected rolling_avg_3 to be {expected_data['rolling_avg_3']}, got {data['rolling_avg_3']}."

    assert data["latest_by_level"] == expected_data["latest_by_level"], \
        f"Expected latest_by_level to be {expected_data['latest_by_level']}, got {data['latest_by_level']}."