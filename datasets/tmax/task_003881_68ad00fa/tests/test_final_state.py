# test_final_state.py

import os
import sqlite3
import math
import csv
import pytest

PIPELINE_DIR = "/home/user/pipeline"
DB_PATH = os.path.join(PIPELINE_DIR, "data.db")
TRAIN_CSV = os.path.join(PIPELINE_DIR, "train_clean.csv")
TEST_CSV = os.path.join(PIPELINE_DIR, "test_clean.csv")

def test_csv_files_exist():
    assert os.path.isfile(TRAIN_CSV), f"Expected output file {TRAIN_CSV} is missing. Did the program run?"
    assert os.path.isfile(TEST_CSV), f"Expected output file {TEST_CSV} is missing. Did the program run?"

def test_csv_contents():
    # Read truth from DB to compute expected values
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, f1, f2, is_train FROM measurements ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    train_f1 = [r[1] for r in rows if r[3] == 1]
    train_f2 = [r[2] for r in rows if r[3] == 1]

    # Compute mean
    mean_f1 = sum(train_f1) / len(train_f1)
    mean_f2 = sum(train_f2) / len(train_f2)

    # Compute sample stddev
    std_f1 = math.sqrt(sum((x - mean_f1)**2 for x in train_f1) / (len(train_f1) - 1))
    std_f2 = math.sqrt(sum((x - mean_f2)**2 for x in train_f2) / (len(train_f2) - 1))

    expected_train = []
    expected_test = []

    for r in rows:
        id_val, f1_val, f2_val, is_train = r
        f1_scaled = (f1_val - mean_f1) / std_f1
        f2_scaled = (f2_val - mean_f2) / std_f2

        row_dict = {
            'id': str(id_val),
            'f1': f"{f1_scaled:.4f}",
            'f2': f"{f2_scaled:.4f}"
        }

        if is_train == 1:
            expected_train.append(row_dict)
        else:
            expected_test.append(row_dict)

    # Helper to read and parse CSV
    def read_csv(filepath):
        with open(filepath, 'r', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)

    actual_train = read_csv(TRAIN_CSV)
    actual_test = read_csv(TEST_CSV)

    assert len(actual_train) == len(expected_train), f"Expected {len(expected_train)} rows in {TRAIN_CSV}, got {len(actual_train)}"
    assert len(actual_test) == len(expected_test), f"Expected {len(expected_test)} rows in {TEST_CSV}, got {len(actual_test)}"

    for i, (actual, expected) in enumerate(zip(actual_train, expected_train)):
        assert actual == expected, f"Row {i+1} in {TRAIN_CSV} mismatch. Expected {expected}, got {actual}. Data leakage might still be present."

    for i, (actual, expected) in enumerate(zip(actual_test, expected_test)):
        assert actual == expected, f"Row {i+1} in {TEST_CSV} mismatch. Expected {expected}, got {actual}. Data leakage might still be present."