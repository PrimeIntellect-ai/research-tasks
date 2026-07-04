# test_final_state.py

import os
import json
import pytest

def test_mapped_errors_jsonl():
    jsonl_path = "/home/user/mapped_errors.jsonl"
    assert os.path.isfile(jsonl_path), f"Output file {jsonl_path} does not exist."

    expected_objects = [
        {"timestamp": "2023-10-01 10:00:00", "level": "ERROR", "category": "Database Issue"},
        {"timestamp": "2023-10-01 10:05:00", "level": "WARNING", "category": "Disk Issue"},
        {"timestamp": "2023-10-01 10:10:00", "level": "CRITICAL", "category": "Memory Issue"},
        {"timestamp": "2023-10-01 10:15:00", "level": "INFO", "category": "Unknown"},
        {"timestamp": "2023-10-01 10:20:00", "level": "ERROR", "category": "Database Issue"}
    ]

    with open(jsonl_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {jsonl_path}, found {len(lines)}."

    for idx, (line, expected) in enumerate(zip(lines, expected_objects)):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {idx+1} is not valid JSON: {line}")

        assert obj == expected, f"Line {idx+1} does not match expected output.\nExpected: {expected}\nGot: {obj}"

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    expected_log = "[INFO] Processed 5 logs, 4 matched, 1 unknown"
    assert expected_log in content, f"Expected log line '{expected_log}' not found in {log_path}."