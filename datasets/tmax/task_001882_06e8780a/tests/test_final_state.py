# test_final_state.py

import os
import csv
import math
import pytest

CLEANED_CSV_PATH = "/home/user/output/cleaned.csv"
SIMILAR_TXT_PATH = "/home/user/output/similar.txt"

def test_cleaned_csv_exists():
    assert os.path.isfile(CLEANED_CSV_PATH), f"Expected output file {CLEANED_CSV_PATH} does not exist."

def test_similar_txt_exists():
    assert os.path.isfile(SIMILAR_TXT_PATH), f"Expected output file {SIMILAR_TXT_PATH} does not exist."

def test_cleaned_csv_contents():
    assert os.path.isfile(CLEANED_CSV_PATH), f"Cannot test content, {CLEANED_CSV_PATH} is missing."

    with open(CLEANED_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 1, "The cleaned.csv file is empty or missing a header."
    header = rows[0]
    expected_header = ["ServerID", "CPU", "Mem", "NetTotal"]
    assert header == expected_header, f"Header in cleaned.csv is incorrect. Expected {expected_header}, got {header}."

    # Expected data rows as a dictionary for easy lookup
    expected_data = {
        "S-01": {"CPU": "45.00", "Mem": "60.00", "NetTotal": "15.00"},
        "S-02": {"CPU": "63.60", "Mem": "70.00", "NetTotal": "21.00"},
        "S-04": {"CPU": "40.00", "Mem": "55.00", "NetTotal": "17.00"},
        "S-05": {"CPU": "42.00", "Mem": "64.60", "NetTotal": "13.00"},
        "S-10": {"CPU": "41.00", "Mem": "58.00", "NetTotal": "15.00"}
    }

    actual_data = {}
    for row in rows[1:]:
        assert len(row) == 4, f"Row {row} does not have exactly 4 columns."
        actual_data[row[0]] = {"CPU": row[1], "Mem": row[2], "NetTotal": row[3]}

    assert "S-03" not in actual_data, "Row S-03 should have been filtered out (CPU > 100.0)."

    assert set(actual_data.keys()) == set(expected_data.keys()), \
        f"ServerIDs in cleaned.csv do not match expected. Expected {list(expected_data.keys())}, got {list(actual_data.keys())}."

    for sid, expected_vals in expected_data.items():
        actual_vals = actual_data[sid]
        for col in ["CPU", "Mem", "NetTotal"]:
            assert actual_vals[col] == expected_vals[col], \
                f"For {sid}, expected {col} to be {expected_vals[col]}, but got {actual_vals[col]}."

def test_similar_txt_contents():
    assert os.path.isfile(SIMILAR_TXT_PATH), f"Cannot test content, {SIMILAR_TXT_PATH} is missing."

    with open(SIMILAR_TXT_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["S-04", "S-01"]

    assert lines == expected_lines, \
        f"Contents of similar.txt do not match expected. Expected {expected_lines}, got {lines}."