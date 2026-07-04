# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_metrics_json_accuracy():
    """Verify that metrics.json contains the correct accuracy score."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.exists(metrics_path), f"File not found: {metrics_path}"

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} is not a valid JSON file.")

    assert 'accuracy' in metrics, "metrics.json does not contain the key 'accuracy'."

    # Expected accuracy is 0.855
    expected_acc = 0.855
    actual_acc = metrics['accuracy']

    assert isinstance(actual_acc, (int, float)), "Accuracy must be a number."
    assert math.isclose(actual_acc, expected_acc, abs_tol=1e-3), \
        f"Expected accuracy close to {expected_acc}, but got {actual_acc}. The data leakage might not be properly fixed."

def test_x_train_fixed_csv():
    """Verify that X_train_fixed.csv exists, has correct dimensions, and is properly scaled."""
    csv_path = '/home/user/X_train_fixed.csv'
    assert os.path.exists(csv_path), f"File not found: {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 800, f"Expected 800 rows in {csv_path}, but got {len(rows)}."

    if len(rows) > 0:
        assert len(rows[0]) == 20, f"Expected 20 columns in {csv_path}, but got {len(rows[0])}."

        # Check that the first column has a mean close to 0 (StandardScaler property)
        try:
            col_0_values = [float(row[0]) for row in rows]
        except ValueError:
            pytest.fail("Could not parse values in the first column as floats.")

        mean_col_0 = sum(col_0_values) / len(col_0_values)
        assert abs(mean_col_0) < 1e-5, \
            f"Expected mean of the first column to be close to 0 (StandardScaler), but got {mean_col_0}."

def test_train_py_updated():
    """Verify that train.py has been modified to fix the data leakage."""
    train_path = '/home/user/train.py'
    assert os.path.exists(train_path), f"File not found: {train_path}"

    with open(train_path, 'r') as f:
        content = f.read()

    # Check that train_test_split is called before scaling
    assert "train_test_split(" in content, "train_test_split is missing in train.py"
    assert "StandardScaler" in content, "StandardScaler is missing in train.py"
    assert "X_train_fixed.csv" in content, "The script does not seem to save X_train_fixed.csv"