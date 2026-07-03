# test_final_state.py

import os
import csv
import pytest

CLEANED_PATH = "/home/user/output/cleaned.csv"
BOOTSTRAP_PATH = "/home/user/output/bootstrap.csv"
REC_PATH = "/home/user/output/recommendations.csv"

def test_cleaned_csv_exists_and_correct():
    assert os.path.isfile(CLEANED_PATH), f"File not found: {CLEANED_PATH}"

    with open(CLEANED_PATH, "r") as f:
        reader = csv.reader(f)
        lines = list(reader)

    assert len(lines) > 0, f"{CLEANED_PATH} is empty"
    header = lines[0]
    assert header == ["user_id", "item_id", "rating"], f"Incorrect header in {CLEANED_PATH}"

    data_lines = lines[1:]
    users = set(row[0] for row in data_lines if len(row) > 0)

    assert "U4" not in users, "User U4 should have been removed (outlier > 5 valid purchases)."
    assert "U5" not in users, "User U5 should have been removed (invalid ratings)."
    assert "U6" not in users, "User U6 should have been removed (invalid rating)."

    assert "U1" in users and "U2" in users and "U3" in users, "Valid users U1, U2, U3 should be in the cleaned dataset."

    # Check that there are exactly 9 valid purchases for U1, U2, U3
    assert len(data_lines) == 9, f"Expected 9 data rows in {CLEANED_PATH}, found {len(data_lines)}"

def test_bootstrap_csv_exists_and_correct():
    assert os.path.isfile(BOOTSTRAP_PATH), f"File not found: {BOOTSTRAP_PATH}"

    with open(BOOTSTRAP_PATH, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 501, f"Expected exactly 501 lines in {BOOTSTRAP_PATH} (1 header + 500 data), found {len(lines)}"
    assert lines[0] == "user_id,item_id,rating", f"Incorrect header in {BOOTSTRAP_PATH}"

    # Check that all sampled rows come from the cleaned dataset
    with open(CLEANED_PATH, "r") as f:
        cleaned_lines = set(f.read().splitlines()[1:])

    for i, line in enumerate(lines[1:], start=2):
        assert line in cleaned_lines, f"Row {i} in {BOOTSTRAP_PATH} ('{line}') is not a valid row from {CLEANED_PATH}"

def test_recommendations_csv_exists_and_correct():
    assert os.path.isfile(REC_PATH), f"File not found: {REC_PATH}"

    with open(REC_PATH, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "recommended_item_id,co_occurrence_count",
        "ITEM_002,3",
        "ITEM_003,2",
        "ITEM_004,1"
    ]

    assert content == expected_content, f"Content of {REC_PATH} does not match expected recommendations."