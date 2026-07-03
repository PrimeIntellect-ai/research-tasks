# test_final_state.py

import os
import csv

def test_prepare_data_cpp_exists():
    cpp_file = "/home/user/prepare_data.cpp"
    assert os.path.isfile(cpp_file), f"Expected C++ source file missing at {cpp_file}"

def test_training_pairs_csv_content():
    output_file = "/home/user/training_pairs.csv"
    assert os.path.isfile(output_file), f"Expected output file missing at {output_file}"

    expected_pairs = [
        {"user_id": "1", "similar_user_id": "2"},
        {"user_id": "2", "similar_user_id": "1"},
        {"user_id": "3", "similar_user_id": "4"},
        {"user_id": "4", "similar_user_id": "1"},
    ]

    with open(output_file, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["user_id", "similar_user_id"], "CSV header is incorrect"

        actual_pairs = list(reader)

    assert len(actual_pairs) == len(expected_pairs), f"Expected {len(expected_pairs)} rows, but got {len(actual_pairs)}"

    for i, (actual, expected) in enumerate(zip(actual_pairs, expected_pairs)):
        assert actual["user_id"] == expected["user_id"], f"Row {i+1} user_id mismatch: expected {expected['user_id']}, got {actual['user_id']}"
        assert actual["similar_user_id"] == expected["similar_user_id"], f"Row {i+1} similar_user_id mismatch for user {actual['user_id']}: expected {expected['similar_user_id']}, got {actual['similar_user_id']}"