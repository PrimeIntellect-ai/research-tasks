# test_final_state.py

import os
import json
from collections import defaultdict
import pytest

def test_rust_project_exists():
    assert os.path.exists("/home/user/aggregator/Cargo.toml"), "Rust project Cargo.toml is missing."
    assert os.path.exists("/home/user/aggregator/src/main.rs"), "Rust project src/main.rs is missing."

def test_pipeline_log():
    log_file = "/home/user/pipeline.log"
    assert os.path.exists(log_file), f"Log file {log_file} is missing."

    with open(log_file, "r") as f:
        logs = f.read()

    expected_logs = [
        "Processed 50000 records",
        "Processed 100000 records",
        "Processed 150000 records"
    ]

    for expected in expected_logs:
        assert expected in logs, f"Expected log statement '{expected}' not found in {log_file}."

def test_aggregated_jsonl():
    csv_file = "/home/user/sensor_data.csv"
    jsonl_file = "/home/user/aggregated.jsonl"

    assert os.path.exists(jsonl_file), f"Output file {jsonl_file} is missing."

    # Compute expected results from the CSV
    data = defaultdict(list)
    with open(csv_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            ts_str, val_str = line.strip().split(",")
            ts = int(ts_str)
            val = float(val_str)
            bucket = ts - (ts % 3600)
            data[bucket].append(val)

    expected = []
    for bucket in sorted(data.keys()):
        vals = data[bucket]
        count = len(vals)
        mean = sum(vals) / count
        variance = sum((x - mean) ** 2 for x in vals) / count
        expected.append({
            "hour_start": bucket,
            "count": count,
            "mean": mean,
            "variance": variance
        })

    # Read agent's output
    agent_output = []
    with open(jsonl_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                agent_output.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line in {jsonl_file}: {line.strip()}")

    assert len(expected) == len(agent_output), f"Length mismatch: expected {len(expected)} records, got {len(agent_output)}."

    for exp, agt in zip(expected, agent_output):
        assert "hour_start" in agt, "Missing 'hour_start' key in JSON output."
        assert "count" in agt, "Missing 'count' key in JSON output."
        assert "mean" in agt, "Missing 'mean' key in JSON output."
        assert "variance" in agt, "Missing 'variance' key in JSON output."

        assert exp["hour_start"] == agt["hour_start"], f"Mismatch in hour_start: expected {exp['hour_start']}, got {agt['hour_start']}."
        assert exp["count"] == agt["count"], f"Mismatch in count for bucket {exp['hour_start']}: expected {exp['count']}, got {agt['count']}."

        assert abs(exp["mean"] - agt["mean"]) <= 1e-4, f"Mean mismatch for bucket {exp['hour_start']}: expected {exp['mean']}, got {agt['mean']}."
        assert abs(exp["variance"] - agt["variance"]) <= 1e-4, f"Variance mismatch for bucket {exp['hour_start']}: expected {exp['variance']}, got {agt['variance']}."