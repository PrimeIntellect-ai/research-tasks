# test_final_state.py
import os
import csv
import math
import pytest

def test_test_transformed_exists():
    """Check that the output file exists."""
    assert os.path.exists("/home/user/test_transformed.csv"), "Output file /home/user/test_transformed.csv is missing."

def test_test_transformed_content():
    """Verify the contents of the transformed test set."""
    # Recompute train statistics
    train_f1 = [float(i) for i in range(1, 801)]
    train_f2 = [float(i * 2) for i in range(1, 801)]

    n_train = len(train_f1)
    mean_f1 = sum(train_f1) / n_train
    mean_f2 = sum(train_f2) / n_train

    var_f1 = sum((x - mean_f1)**2 for x in train_f1) / (n_train - 1)
    var_f2 = sum((x - mean_f2)**2 for x in train_f2) / (n_train - 1)

    std_f1 = math.sqrt(var_f1)
    std_f2 = math.sqrt(var_f2)

    # Generate expected test rows
    expected_rows = []
    for i in range(801, 1001):
        f1 = float(i)
        f2 = float(i * 2)
        label = i % 2

        f1_scaled = (f1 - mean_f1) / std_f1
        f2_scaled = (f2 - mean_f2) / std_f2
        reduced_f = (f1_scaled + f2_scaled) / 2.0

        expected_rows.append([f"{reduced_f:.4f}", str(label)])

    # Read actual test rows
    actual_rows = []
    with open("/home/user/test_transformed.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["reduced_f", "label"], f"Expected header ['reduced_f', 'label'], got {header}"

        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == 200, f"Expected exactly 200 rows in the test set, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i + 1} mismatch: expected {expected}, got {actual}"