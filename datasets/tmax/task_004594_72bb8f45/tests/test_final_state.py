# test_final_state.py

import json
import os
import math

def test_metrics_json_exists():
    """Verify that the metrics.json file was created successfully."""
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), f"{metrics_path} does not exist. Did the script run and output the file?"
    assert os.path.isfile(metrics_path), f"{metrics_path} is not a file."

def test_metrics_json_content():
    """Verify that the metrics.json file contains the correct calculated metrics."""
    logs_path = "/home/user/ping_logs.jsonl"
    metrics_path = "/home/user/metrics.json"

    assert os.path.isfile(logs_path), f"{logs_path} is missing."

    # Read the input logs to derive the expected output
    with open(logs_path, "r") as f:
        logs = [json.loads(line) for line in f if line.strip()]

    # Read the output metrics
    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} does not contain valid JSON."

    assert isinstance(metrics, list), f"Expected {metrics_path} to contain a JSON array, but got {type(metrics).__name__}."
    assert len(metrics) == len(logs), f"Expected {len(logs)} metric entries, found {len(metrics)}."

    successful = 0
    total = 0
    latencies = []

    for i, (log, metric) in enumerate(zip(logs, metrics)):
        total += 1
        if log.get("status") == "success":
            successful += 1
        latencies.append(log.get("latency", 0))

        # Recompute expected values
        expected_uptime = successful / total

        # Rolling average of up to the last 5 pings
        window_size = 5
        window = latencies[-window_size:] if len(latencies) >= window_size else latencies
        expected_rolling_avg = sum(window) / len(window)

        # Validate structure
        assert "timestamp" in metric, f"Entry {i} is missing the 'timestamp' key."
        assert isinstance(metric["timestamp"], str), f"Entry {i} 'timestamp' must be a string. Are datetime objects properly serialized?"

        assert "cumulative_uptime" in metric, f"Entry {i} is missing the 'cumulative_uptime' key."
        assert isinstance(metric["cumulative_uptime"], (int, float)), f"Entry {i} 'cumulative_uptime' must be a number."

        assert "rolling_latency_avg" in metric, f"Entry {i} is missing the 'rolling_latency_avg' key."
        assert isinstance(metric["rolling_latency_avg"], (int, float)), f"Entry {i} 'rolling_latency_avg' must be a number."

        # Validate mathematical correctness
        assert math.isclose(metric["cumulative_uptime"], expected_uptime, rel_tol=1e-5, abs_tol=1e-5), \
            f"Entry {i}: Incorrect 'cumulative_uptime'. Expected {expected_uptime}, got {metric['cumulative_uptime']}."

        assert math.isclose(metric["rolling_latency_avg"], expected_rolling_avg, rel_tol=1e-5, abs_tol=1e-5), \
            f"Entry {i}: Incorrect 'rolling_latency_avg'. Expected {expected_rolling_avg}, got {metric['rolling_latency_avg']}. Check boundary conditions."