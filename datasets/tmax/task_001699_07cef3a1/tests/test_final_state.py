# test_final_state.py

import os
import json
import pytest

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline.py"), "/home/user/pipeline.py does not exist."

def test_artifact_metrics_json_exists_and_valid():
    metrics_path = "/home/user/artifact_metrics.json"
    assert os.path.isfile(metrics_path), f"{metrics_path} does not exist."

    with open(metrics_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} does not contain valid JSON.")

    assert isinstance(data, dict), f"JSON root in {metrics_path} must be an object (dictionary)."

def test_artifact_metrics_content():
    metrics_path = "/home/user/artifact_metrics.json"
    assert os.path.isfile(metrics_path), f"{metrics_path} does not exist."

    with open(metrics_path, "r") as f:
        data = json.load(f)

    expected = {
        "model_fast.bin": {
            "size_bytes": 1500,
            "latency_ms": 44.0,
            "throughput": 1136.36
        },
        "model_balanced.bin": {
            "size_bytes": 4500,
            "latency_ms": 108.0,
            "throughput": 462.96
        },
        "model_heavy.bin": {
            "size_bytes": 12000,
            "latency_ms": 255.0,
            "throughput": 196.08
        }
    }

    # Check keys
    assert set(data.keys()) == set(expected.keys()), f"Keys in {metrics_path} do not match expected models. Got {list(data.keys())}, expected {list(expected.keys())}"

    # Check values
    for model_name, expected_metrics in expected.items():
        actual_metrics = data[model_name]
        assert isinstance(actual_metrics, dict), f"Value for {model_name} is not a JSON object."

        # Check size_bytes
        assert "size_bytes" in actual_metrics, f"Missing 'size_bytes' for {model_name}"
        assert actual_metrics["size_bytes"] == expected_metrics["size_bytes"], f"Incorrect size_bytes for {model_name}"

        # Check latency_ms (allowing small float differences)
        assert "latency_ms" in actual_metrics, f"Missing 'latency_ms' for {model_name}"
        assert abs(actual_metrics["latency_ms"] - expected_metrics["latency_ms"]) < 0.01, f"Incorrect latency_ms for {model_name}"

        # Check throughput (allowing small float differences)
        assert "throughput" in actual_metrics, f"Missing 'throughput' for {model_name}"
        assert abs(actual_metrics["throughput"] - expected_metrics["throughput"]) < 0.01, f"Incorrect throughput for {model_name}"