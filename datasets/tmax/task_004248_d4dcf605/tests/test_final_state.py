# test_final_state.py

import os
import json
import re
import subprocess
import math
from datetime import datetime, timedelta
import pytest

def get_expected_metrics(log_path):
    if not os.path.exists(log_path):
        return []

    endpoint_pattern = re.compile(r"^/api/v[1-3]/[a-z_]+$")
    log_pattern = re.compile(r"\[(.*?)\] .*?endpoint=(\S+) latency_ms=(\d+)")

    buckets = {}

    with open(log_path, "r") as f:
        for line in f:
            match = log_pattern.search(line)
            if not match:
                continue

            ts_str, endpoint, latency_str = match.groups()
            latency = int(latency_str)

            if not endpoint_pattern.match(endpoint):
                continue

            dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
            minute_floored = (dt.minute // 5) * 5
            bucket_dt = dt.replace(minute=minute_floored, second=0)
            bucket_str = bucket_dt.strftime("%Y-%m-%d %H:%M:%S")

            key = (bucket_str, endpoint)
            if key not in buckets:
                buckets[key] = {"count": 0, "sum_latency": 0}

            buckets[key]["count"] += 1
            buckets[key]["sum_latency"] += latency

    expected = []
    for (bucket, endpoint), data in buckets.items():
        avg_latency = math.floor(data["sum_latency"] / data["count"])
        expected.append({
            "bucket": bucket,
            "endpoint": endpoint,
            "request_count": data["count"],
            "avg_latency": avg_latency
        })

    # Sort to make comparison easy
    expected.sort(key=lambda x: (x["bucket"], x["endpoint"]))
    return expected

def test_makefile_execution():
    """Test that the Makefile exists and can run 'clean' and 'all' successfully."""
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing in /home/user."

    # Run make clean
    clean_result = subprocess.run(
        ["make", "clean"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    # We don't strictly assert clean_result.returncode == 0 because clean might fail if files don't exist,
    # but a good Makefile handles that. We will just ensure 'make all' works.

    # Run make all
    all_result = subprocess.run(
        ["make", "all"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert all_result.returncode == 0, f"'make all' failed with output:\n{all_result.stderr}\n{all_result.stdout}"

def test_final_metrics_json():
    """Test that final_metrics.json is created, is valid JSON, and contains the correct aggregated data."""
    json_path = "/home/user/final_metrics.json"
    assert os.path.isfile(json_path), f"{json_path} was not generated."

    with open(json_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"{json_path} is not valid JSON: {e}")

    assert isinstance(actual_data, list), "The JSON output should be a list of objects."

    # Normalize actual data (sort by bucket and endpoint)
    try:
        actual_data.sort(key=lambda x: (x["bucket"], x["endpoint"]))
    except KeyError as e:
        pytest.fail(f"Missing expected key in JSON objects: {e}")

    expected_data = get_expected_metrics("/home/user/raw_server.log")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(actual_data)}."

    for actual, expected in zip(actual_data, expected_data):
        assert actual["bucket"] == expected["bucket"], f"Expected bucket {expected['bucket']}, got {actual['bucket']}"
        assert actual["endpoint"] == expected["endpoint"], f"Expected endpoint {expected['endpoint']}, got {actual['endpoint']}"
        assert actual["request_count"] == expected["request_count"], f"Expected request_count {expected['request_count']} for {expected['endpoint']}, got {actual['request_count']}"
        assert actual["avg_latency"] == expected["avg_latency"], f"Expected avg_latency {expected['avg_latency']} for {expected['endpoint']}, got {actual['avg_latency']}"