# test_final_state.py

import os
import pytest

def test_processed_files_exist():
    assert os.path.isfile("/home/user/train_processed.csv"), "/home/user/train_processed.csv is missing. Did the script run and save the output?"
    assert os.path.isfile("/home/user/test_processed.csv"), "/home/user/test_processed.csv is missing. Did the script run and save the output?"

def test_row_counts():
    with open("/home/user/train_processed.csv", "r") as f:
        train_lines = f.readlines()
    with open("/home/user/test_processed.csv", "r") as f:
        test_lines = f.readlines()

    assert len(train_lines) == 800, f"Expected exactly 800 rows in train_processed.csv, but found {len(train_lines)}."
    assert len(test_lines) == 200, f"Expected exactly 200 rows in test_processed.csv, but found {len(test_lines)}."

def test_data_processing_correctness():
    dataset_path = "/home/user/dataset.csv"
    assert os.path.isfile(dataset_path), f"Original dataset {dataset_path} is missing."

    with open(dataset_path, "r") as f:
        dataset_lines = [line.strip().split(',') for line in f.readlines() if line.strip()]

    assert len(dataset_lines) == 1000, "Original dataset does not have 1000 rows. It might have been modified incorrectly."

    train_data = dataset_lines[:800]
    test_data = dataset_lines[800:]

    # Calculate min and max strictly from the training set
    train_c3 = [float(row[2]) for row in train_data]
    train_min = min(train_c3)
    train_max = max(train_c3)

    def process_row(row):
        # Scale using train min/max and drop 5th column
        scaled_val = (float(row[2]) - train_min) / (train_max - train_min)
        # Format to 4 decimal places
        scaled_str = f"{scaled_val:.4f}"
        return f"{row[0]},{row[1]},{scaled_str},{row[3]}\n"

    expected_train = [process_row(row) for row in train_data]
    expected_test = [process_row(row) for row in test_data]

    with open("/home/user/train_processed.csv", "r") as f:
        actual_train = f.readlines()

    with open("/home/user/test_processed.csv", "r") as f:
        actual_test = f.readlines()

    # Verify Train Set
    for i, (exp, act) in enumerate(zip(expected_train, actual_train)):
        act_cols = act.strip().split(',')
        assert len(act_cols) == 4, f"Train row {i+1} has {len(act_cols)} columns instead of 4. Column 5 was likely not dropped."
        assert act == exp, f"Train row {i+1} mismatch.\nExpected: {exp.strip()}\nGot:      {act.strip()}"

    # Verify Test Set
    for i, (exp, act) in enumerate(zip(expected_test, actual_test)):
        act_cols = act.strip().split(',')
        assert len(act_cols) == 4, f"Test row {i+1} has {len(act_cols)} columns instead of 4. Column 5 was likely not dropped."
        assert act == exp, f"Test row {i+1} mismatch.\nExpected: {exp.strip()}\nGot:      {act.strip()}"