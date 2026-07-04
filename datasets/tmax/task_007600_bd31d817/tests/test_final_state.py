# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_scripts_and_makefile_exist():
    """Verify that the required scripts and Makefile exist."""
    for filename in ['etl.py', 'train.py', 'Makefile']:
        path = f"/home/user/{filename}"
        assert os.path.exists(path), f"Required file {path} is missing."
        assert os.path.isfile(path), f"{path} is not a regular file."

def test_processed_data_exists_and_structure():
    """Verify that processed_data.csv exists and has the correct columns and no missing values."""
    processed_path = "/home/user/processed_data.csv"
    assert os.path.exists(processed_path), f"File {processed_path} is missing."

    expected_columns = {"sensor_id", "temperature", "vibration", "pressure", "status", "remaining_life"}

    with open(processed_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None, f"{processed_path} has no header."

        actual_columns = set(reader.fieldnames)
        missing_columns = expected_columns - actual_columns
        assert not missing_columns, f"Processed data is missing columns: {missing_columns}"

        for row_idx, row in enumerate(reader, start=2):
            for col in expected_columns:
                val = row[col].strip()
                assert val != "", f"Missing value found in row {row_idx}, column {col}."
                # Ensure it's numeric
                try:
                    float(val)
                except ValueError:
                    pytest.fail(f"Non-numeric value '{val}' found in row {row_idx}, column {col}.")

def test_experiments_jsonl_structure():
    """Verify that experiments.jsonl exists and contains the correct JSON structure."""
    jsonl_path = "/home/user/experiments.jsonl"
    assert os.path.exists(jsonl_path), f"File {jsonl_path} is missing."

    lines = []
    with open(jsonl_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(json.loads(line))

    assert len(lines) >= 2, f"Expected at least 2 JSON lines in {jsonl_path}, found {len(lines)}."

    # Look for the latest classification and regression results
    cls_result = None
    reg_result = None

    for entry in lines:
        if entry.get("model_type") == "LogisticRegression" and entry.get("target") == "status":
            cls_result = entry
        elif entry.get("model_type") == "Ridge" and entry.get("target") == "remaining_life":
            reg_result = entry

    assert cls_result is not None, "Missing LogisticRegression result for 'status' in experiments.jsonl."
    assert reg_result is not None, "Missing Ridge result for 'remaining_life' in experiments.jsonl."

    assert cls_result.get("metric_name") == "accuracy", f"Expected metric_name 'accuracy', got {cls_result.get('metric_name')}"
    assert isinstance(cls_result.get("metric_value"), (int, float)), "Classification metric_value must be a number."

    assert reg_result.get("metric_name") == "mse", f"Expected metric_name 'mse', got {reg_result.get('metric_name')}"
    assert isinstance(reg_result.get("metric_value"), (int, float)), "Regression metric_value must be a number."

def test_makefile_targets():
    """Verify that the Makefile contains the required targets."""
    makefile_path = "/home/user/Makefile"
    with open(makefile_path, "r") as f:
        content = f.read()

    assert "etl:" in content, "Makefile is missing 'etl' target."
    assert "train:" in content, "Makefile is missing 'train' target."
    assert "all:" in content, "Makefile is missing 'all' target."