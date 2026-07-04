# test_final_state.py
import os
import json
import urllib.parse

def test_metrics_json():
    metrics_path = "/home/user/data/metrics.json"
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse JSON in {metrics_path}: {e}"

    expected_metrics = {
        "total_processed": 4,
        "fast_count": 2,
        "medium_count": 1,
        "slow_count": 1
    }

    for key, expected_val in expected_metrics.items():
        assert key in metrics, f"Missing key '{key}' in metrics.json"
        assert metrics[key] == expected_val, f"Expected {key} to be {expected_val}, got {metrics[key]}"

def test_processed_logs_jsonl():
    processed_path = "/home/user/data/processed_logs.jsonl"
    assert os.path.isfile(processed_path), f"Processed logs file {processed_path} is missing."

    with open(processed_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {processed_path}, found {len(lines)}."

    expected_records = [
        {
            "timestamp": "2023-10-12T12:30:00Z",
            "ip_address": "192.168.1.0",
            "masked_email": "***@example.com",
            "path": "/v1/users",
            "response_time_ms": 45,
            "speed": "fast"
        },
        {
            "timestamp": "2023-10-12T12:30:00Z",
            "ip_address": "10.0.0.0",
            "masked_email": "***@work.org",
            "path": "/reports/q3",
            "response_time_ms": 150,
            "speed": "medium"
        },
        {
            "timestamp": "2023-10-12T12:30:00Z",
            "ip_address": "172.16.254.0",
            "masked_email": "***@test.io",
            "path": "/",
            "response_time_ms": 600,
            "speed": "slow"
        },
        {
            "timestamp": "2023-10-12T12:30:00Z",
            "ip_address": "8.8.8.0",
            "masked_email": "***@sys.local",
            "path": "/v1/status",
            "response_time_ms": 99,
            "speed": "fast"
        }
    ]

    for i, (line, expected) in enumerate(zip(lines, expected_records)):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse JSON on line {i+1} of {processed_path}: {e}"

        # Check exact keys
        expected_keys = set(expected.keys())
        record_keys = set(record.keys())
        assert record_keys == expected_keys, f"Line {i+1} has incorrect keys. Expected {expected_keys}, got {record_keys}"

        # Check values
        for key in expected_keys:
            assert record[key] == expected[key], f"Line {i+1} field '{key}' mismatch. Expected {expected[key]}, got {record[key]}"