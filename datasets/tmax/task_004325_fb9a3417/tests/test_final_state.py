# test_final_state.py

import os
import json
import re
import requests
import pytest
from collections import defaultdict

def compute_expected_stats():
    log_path = "/home/user/access.log"
    if not os.path.exists(log_path):
        pytest.fail(f"Log file {log_path} is missing, cannot compute expected stats.")

    with open(log_path, "r") as f:
        lines = f.readlines()

    # Remove exact duplicates while preserving order
    unique_lines = list(dict.fromkeys(lines))

    stats = defaultdict(lambda: {"total_requests": 0, "error_count": 0, "response_time_sum": 0})

    # Regex to parse: [2023-10-01 10:00:05] 192.168.1.1 "GET /index.html HTTP/1.1" 200 120
    pattern = re.compile(r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}):\d{2}\] \S+ "[^"]+" (\d+) (\d+)')

    for line in unique_lines:
        match = pattern.search(line.strip())
        if match:
            minute, status_str, time_str = match.groups()
            status = int(status_str)
            time_ms = int(time_str)

            stats[minute]["total_requests"] += 1
            if status >= 400:
                stats[minute]["error_count"] += 1
            stats[minute]["response_time_sum"] += time_ms

    result = []
    for minute in sorted(stats.keys()):
        data = stats[minute]
        avg_time = data["response_time_sum"] // data["total_requests"]
        result.append({
            "minute": minute,
            "total_requests": data["total_requests"],
            "error_count": data["error_count"],
            "avg_response_time": avg_time
        })

    return result

@pytest.fixture(scope="module")
def expected_stats():
    return compute_expected_stats()

def test_stats_json_file(expected_stats):
    """Check if the stats.json file is correctly generated."""
    stats_path = "/home/user/stats.json"
    assert os.path.isfile(stats_path), f"File {stats_path} is missing."

    with open(stats_path, "r") as f:
        try:
            actual_stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {stats_path} does not contain valid JSON.")

    assert actual_stats == expected_stats, f"Data in {stats_path} does not match expected output."

def test_http_server_stats(expected_stats):
    """Check if the HTTP server is running and serves the correct stats."""
    url = "http://127.0.0.1:8080/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        actual_stats = response.json()
    except ValueError:
        pytest.fail("HTTP response body is not valid JSON.")

    assert actual_stats == expected_stats, "HTTP response JSON does not match expected output."