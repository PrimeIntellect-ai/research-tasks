# test_final_state.py

import os
import json
import pytest

def test_unified_jsonl_exists_and_correct():
    file_path = "/home/user/unified.jsonl"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    expected_data = [
        {"timestamp": 1000, "cpu": 10.0, "memory": 100},
        {"timestamp": 2000, "cpu": 15.0, "memory": 100},
        {"timestamp": 3000, "cpu": 20.0, "memory": 120},
        {"timestamp": 4000, "cpu": 25.0, "memory": 130},
        {"timestamp": 5000, "cpu": 30.0, "memory": 140},
        {"timestamp": 6000, "cpu": 35.0, "memory": 140}
    ]

    actual_data = []
    with open(file_path, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_data.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON on line {line_num} of {file_path}: {line}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("timestamp") == expected["timestamp"], f"Record {i} timestamp mismatch: expected {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual.get("cpu") == expected["cpu"], f"Record {i} cpu mismatch: expected {expected['cpu']}, got {actual.get('cpu')}"
        assert actual.get("memory") == expected["memory"], f"Record {i} memory mismatch: expected {expected['memory']}, got {actual.get('memory')}"

        # Verify types
        assert isinstance(actual["timestamp"], int), f"Record {i} timestamp must be an int."
        assert isinstance(actual["cpu"], float), f"Record {i} cpu must be a float."
        assert isinstance(actual["memory"], int), f"Record {i} memory must be an int."

def test_dag_trace_exists_and_valid():
    file_path = "/home/user/dag_trace.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        tasks = [line.strip() for line in f if line.strip()]

    assert "extract_a" in tasks, "Task 'extract_a' is missing from dag_trace.txt"
    assert "extract_b" in tasks, "Task 'extract_b' is missing from dag_trace.txt"
    assert "transform_impute" in tasks, "Task 'transform_impute' is missing from dag_trace.txt"
    assert "load_results" in tasks, "Task 'load_results' is missing from dag_trace.txt"

    idx_a = tasks.index("extract_a")
    idx_b = tasks.index("extract_b")
    idx_transform = tasks.index("transform_impute")
    idx_load = tasks.index("load_results")

    assert idx_a < idx_transform, "'extract_a' must run before 'transform_impute'."
    assert idx_b < idx_transform, "'extract_b' must run before 'transform_impute'."
    assert idx_transform < idx_load, "'transform_impute' must run before 'load_results'."

def test_pipeline_script_exists():
    file_path = "/home/user/pipeline.py"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."