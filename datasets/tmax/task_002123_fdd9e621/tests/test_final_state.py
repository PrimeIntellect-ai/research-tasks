# test_final_state.py
import os
import json
import pytest

def test_pipeline_script_exists():
    """Check if the student wrote the pipeline test script."""
    script_path = "/home/user/pipeline_test.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_output_csv_content():
    """Check if the output CSV contains only the valid rows and no index."""
    output_file = "/home/user/output.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    with open(output_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "id,value,category",
        "1,12.5,X",
        "3,8.1,Z",
        "5,0.0,X"
    ]

    assert lines == expected_lines, (
        f"Content of {output_file} is incorrect. "
        f"Expected {expected_lines}, but got {lines}."
    )

def test_metrics_json_content():
    """Check if the metrics JSON file has the correct keys and values."""
    metrics_file = "/home/user/metrics.json"
    assert os.path.isfile(metrics_file), f"Metrics file {metrics_file} was not created."

    with open(metrics_file, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_file} is not valid JSON.")

    expected_metrics = {
        "original_rows": 5,
        "valid_rows": 3,
        "schema_passed": True
    }

    for key, expected_value in expected_metrics.items():
        assert key in metrics, f"Key '{key}' is missing from {metrics_file}."
        assert metrics[key] == expected_value, (
            f"Value for '{key}' in {metrics_file} is incorrect. "
            f"Expected {expected_value}, got {metrics[key]}."
        )