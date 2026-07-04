# test_final_state.py

import os
import math
import pytest

def test_output_files_exist():
    assert os.path.isfile("/home/user/data/train_normalized.csv"), "The file /home/user/data/train_normalized.csv was not created."
    assert os.path.isfile("/home/user/data/test_normalized.csv"), "The file /home/user/data/test_normalized.csv was not created."

def test_normalized_data_correctness():
    input_csv = "/home/user/data/input.csv"
    train_csv = "/home/user/data/train_normalized.csv"
    test_csv = "/home/user/data/test_normalized.csv"

    # Read input data
    with open(input_csv, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 101, "Input file should have 101 lines (1 header + 100 data rows)."

    header = lines[0]
    data_lines = lines[1:]

    # Extract values
    values = []
    for line in data_lines:
        parts = line.split(',')
        values.append(float(parts[2]))

    # Calculate training parameters (first 80 rows)
    train_values = values[:80]
    train_mean = sum(train_values) / len(train_values)
    train_variance = sum((x - train_mean) ** 2 for x in train_values) / len(train_values)
    train_std_dev = math.sqrt(train_variance)

    # Read train_normalized.csv
    with open(train_csv, "r") as f:
        train_out_lines = f.read().strip().split('\n')

    assert train_out_lines[0] == "id,category,normalized_value", "Header in train_normalized.csv is incorrect."
    assert len(train_out_lines) == 81, f"Expected 81 lines in train_normalized.csv, found {len(train_out_lines)}."

    for i in range(80):
        expected_norm = (values[i] - train_mean) / train_std_dev
        expected_str = f"{expected_norm:.4f}"

        out_parts = train_out_lines[i + 1].split(',')
        assert len(out_parts) == 3, f"Malformed line in train_normalized.csv: {train_out_lines[i + 1]}"
        assert out_parts[2] == expected_str, f"Row {i + 1} in train_normalized.csv has wrong normalized value. Expected {expected_str}, got {out_parts[2]}. This indicates data leakage or incorrect calculation."

    # Read test_normalized.csv
    with open(test_csv, "r") as f:
        test_out_lines = f.read().strip().split('\n')

    assert test_out_lines[0] == "id,category,normalized_value", "Header in test_normalized.csv is incorrect."
    assert len(test_out_lines) == 21, f"Expected 21 lines in test_normalized.csv, found {len(test_out_lines)}."

    for i in range(20):
        idx = i + 80
        expected_norm = (values[idx] - train_mean) / train_std_dev
        expected_str = f"{expected_norm:.4f}"

        out_parts = test_out_lines[i + 1].split(',')
        assert len(out_parts) == 3, f"Malformed line in test_normalized.csv: {test_out_lines[i + 1]}"
        assert out_parts[2] == expected_str, f"Row {i + 1} in test_normalized.csv has wrong normalized value. Expected {expected_str}, got {out_parts[2]}. This indicates data leakage or incorrect calculation."