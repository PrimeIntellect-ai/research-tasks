# test_final_state.py

import os
import json
import pytest

def test_jq_installed_and_executable():
    """Assert /home/user/bin/jq exists and is executable."""
    jq_path = "/home/user/bin/jq"
    assert os.path.isfile(jq_path), f"jq binary not found at {jq_path}"
    assert os.access(jq_path, os.X_OK), f"jq binary at {jq_path} is not executable"

def test_scripts_exist():
    """Assert the required Bash scripts exist."""
    process_script = "/home/user/process_metrics.sh"
    test_script = "/home/user/test_pipeline.sh"

    assert os.path.isfile(process_script), f"Process script not found at {process_script}"
    assert os.path.isfile(test_script), f"Test script not found at {test_script}"

def test_cleaned_metrics_json():
    """Assert /home/user/cleaned_metrics.json is valid JSON and matches expected records."""
    json_path = "/home/user/cleaned_metrics.json"
    assert os.path.isfile(json_path), f"JSON output not found at {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"JSON root must be an array, got {type(data)}"
    assert len(data) == 4, f"Expected 4 records in JSON array, found {len(data)}"

    expected_records = [
        {"run": "runA", "loss": 0.85, "acc": 0.72},
        {"run": "runA", "loss": 0.5, "acc": 0.75},
        {"run": "runB", "loss": 0.9, "acc": 0.6},
        {"run": "runB", "loss": 0.5, "acc": 0.85}
    ]

    for i, expected in enumerate(expected_records):
        record = data[i]
        assert record.get("run") == expected["run"], f"Record {i}: expected run '{expected['run']}', got '{record.get('run')}'"
        assert float(record.get("loss")) == expected["loss"], f"Record {i}: expected loss {expected['loss']}, got {record.get('loss')}"
        assert float(record.get("acc")) == expected["acc"], f"Record {i}: expected acc {expected['acc']}, got {record.get('acc')}"

def test_test_results_log():
    """Assert /home/user/test_results.log contains the expected test output."""
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Test results log not found at {log_path}"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_str = "Test passed: 4 valid records found."
    assert expected_str in content, f"Expected string '{expected_str}' not found in {log_path}. Content was: '{content}'"