# test_final_state.py

import os
import json
import csv
import pytest

def test_metrics_json_exists_and_valid():
    path = '/home/user/metrics.json'
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    assert "accuracy" in metrics, f"Missing 'accuracy' key in {path}"
    assert "inference_time_seconds" in metrics, f"Missing 'inference_time_seconds' key in {path}"

    # Check accuracy value
    # Due to floating point precision, we can use pytest.approx or check rounding
    assert round(metrics["accuracy"], 3) == 0.685, f"Expected accuracy to be approx 0.685, got {metrics['accuracy']}"

    # Check inference time is a positive number
    assert isinstance(metrics["inference_time_seconds"], (int, float)), "inference_time_seconds must be a number"
    assert metrics["inference_time_seconds"] > 0, "inference_time_seconds must be greater than 0"

def test_predictions_csv_exists_and_valid():
    path = '/home/user/predictions.csv'
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{path} is empty"

    header = rows[0]
    assert header == ["user_id", "predicted_churn"], f"Expected header ['user_id', 'predicted_churn'], got {header}"

    # 200 test samples + 1 header
    assert len(rows) == 201, f"Expected exactly 201 rows (including header), got {len(rows)}"

    # Check that the data rows are properly formatted
    for i, row in enumerate(rows[1:], start=2):
        assert len(row) == 2, f"Row {i} does not have exactly 2 columns"
        assert row[0].isdigit(), f"Row {i} user_id '{row[0]}' is not an integer"
        assert row[1] in ["0", "1", "0.0", "1.0", "False", "True"], f"Row {i} predicted_churn '{row[1]}' is not a valid binary prediction"