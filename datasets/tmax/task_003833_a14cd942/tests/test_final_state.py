# test_final_state.py
import json
import os
import pytest

def test_metrics_json_exists_and_valid():
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} does not exist. Did you run the benchmark?"

    try:
        with open(metrics_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {metrics_path}: {e}")

    assert "total_time_seconds" in data, "metrics.json must contain 'total_time_seconds' key."

    try:
        time = float(data["total_time_seconds"])
    except ValueError:
        pytest.fail(f"'total_time_seconds' must be a float, got {data['total_time_seconds']}")

    threshold = 1.5
    assert time <= threshold, f"Execution time {time} seconds exceeds the threshold of {threshold} seconds."