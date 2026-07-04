# test_final_state.py
import os
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_processed_files_exist():
    assert os.path.isfile("/home/user/train_processed.csv"), "/home/user/train_processed.csv is missing."
    assert os.path.isfile("/home/user/test_processed.csv"), "/home/user/test_processed.csv is missing."

def test_data_leakage_and_preprocessing():
    data_path = "/home/user/data.csv"
    assert os.path.isfile(data_path), f"Original data file {data_path} is missing."

    with open(data_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    assert len(rows) == 100, f"Expected 100 data rows in original dataset, found {len(rows)}."

    train_rows = rows[:80]
    test_rows = rows[80:]

    # Calculate train statistics
    train_values = [float(row[1]) for row in train_rows if row[1].strip() != ""]
    train_mean = sum(train_values) / len(train_values)
    train_min = min(train_values)
    train_max = max(train_values)

    def process_row(row):
        val_str = row[1].strip()
        val = float(val_str) if val_str != "" else train_mean
        scaled = (val - train_min) / (train_max - train_min)
        return [row[0], f"{scaled:.4f}"]

    expected_train = [process_row(row) for row in train_rows]
    expected_test = [process_row(row) for row in test_rows]

    # Check train_processed.csv
    with open("/home/user/train_processed.csv", "r") as f:
        reader = csv.reader(f)
        train_out_header = next(reader)
        train_out_rows = list(reader)

    assert train_out_header == ["id", "value"], "train_processed.csv header is incorrect."
    assert len(train_out_rows) == 80, f"Expected 80 data rows in train_processed.csv, found {len(train_out_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_train, train_out_rows)):
        assert actual == expected, f"Train row {i+1} mismatch. Expected {expected}, got {actual}."

    # Check test_processed.csv
    with open("/home/user/test_processed.csv", "r") as f:
        reader = csv.reader(f)
        test_out_header = next(reader)
        test_out_rows = list(reader)

    assert test_out_header == ["id", "value"], "test_processed.csv header is incorrect."
    assert len(test_out_rows) == 20, f"Expected 20 data rows in test_processed.csv, found {len(test_out_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_test, test_out_rows)):
        assert actual == expected, f"Test row {i+1} mismatch. Expected {expected}, got {actual}."