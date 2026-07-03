# test_final_state.py
import os
import csv
import math
import pytest

def test_normalized_outputs():
    data_path = "/home/user/data.csv"
    assert os.path.isfile(data_path), f"{data_path} is missing. Did you accidentally delete it?"

    with open(data_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{data_path} is empty."

    train_size = int(len(rows) * 0.8)

    # Calculate train mean and std (population std)
    train_values = [float(row['value']) for row in rows[:train_size]]
    train_mean = sum(train_values) / train_size
    train_var = sum((v - train_mean) ** 2 for v in train_values) / train_size
    train_std = math.sqrt(train_var)

    # Check train_norm.csv
    train_norm_path = "/home/user/train_norm.csv"
    assert os.path.isfile(train_norm_path), f"{train_norm_path} is missing. Did you compile and run the program?"

    with open(train_norm_path, "r") as f:
        reader = csv.DictReader(f)
        train_norm_rows = list(reader)

    assert len(train_norm_rows) == train_size, f"{train_norm_path} has incorrect number of rows."

    for i, row in enumerate(train_norm_rows):
        expected_val = (float(rows[i]['value']) - train_mean) / train_std
        actual_val = float(row['value'])
        assert math.isclose(actual_val, expected_val, abs_tol=1e-3), \
            f"Row {i+1} in train_norm.csv has incorrect normalized value. Expected ~{expected_val:.4f}, got {actual_val:.4f}. Check your mean and std calculations."
        assert row['id'] == rows[i]['id'], f"Row {i+1} in train_norm.csv has incorrect id."
        assert row['label'] == rows[i]['label'], f"Row {i+1} in train_norm.csv has incorrect label."

    # Check test_norm.csv
    test_norm_path = "/home/user/test_norm.csv"
    assert os.path.isfile(test_norm_path), f"{test_norm_path} is missing. Did you compile and run the program?"

    with open(test_norm_path, "r") as f:
        reader = csv.DictReader(f)
        test_norm_rows = list(reader)

    assert len(test_norm_rows) == len(rows) - train_size, f"{test_norm_path} has incorrect number of rows."

    for i, row in enumerate(test_norm_rows):
        orig_idx = train_size + i
        expected_val = (float(rows[orig_idx]['value']) - train_mean) / train_std
        actual_val = float(row['value'])
        assert math.isclose(actual_val, expected_val, abs_tol=1e-3), \
            f"Row {i+1} in test_norm.csv has incorrect normalized value. Expected ~{expected_val:.4f}, got {actual_val:.4f}. This indicates data leakage is still present or statistics are wrong."
        assert row['id'] == rows[orig_idx]['id'], f"Row {i+1} in test_norm.csv has incorrect id."
        assert row['label'] == rows[orig_idx]['label'], f"Row {i+1} in test_norm.csv has incorrect label."