# test_final_state.py

import os
import pytest

def test_cleaned_output_csv():
    file_path = "/home/user/cleaned_output.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 1, "cleaned_output.csv is empty or missing header."
    assert lines[0] == "user_id,age,region,score,class_label", "Header is incorrect or missing."

    expected_data = [
        (1, 25, "NA", 0.85, 1),
        (6, 30, "SA", 0.3, 0),
        (9, 22, "NA", 0.77, 1)
    ]

    assert len(lines) - 1 == len(expected_data), f"Expected {len(expected_data)} data rows, found {len(lines) - 1}."

    for i, expected_row in enumerate(expected_data):
        actual_parts = lines[i + 1].split(',')
        assert len(actual_parts) == 5, f"Row {i + 1} does not have 5 columns."

        user_id, age, region, score, class_label = actual_parts
        assert int(user_id) == expected_row[0], f"Row {i + 1} user_id mismatch."
        assert int(age) == expected_row[1], f"Row {i + 1} age mismatch."
        assert region == expected_row[2], f"Row {i + 1} region mismatch."
        assert abs(float(score) - expected_row[3]) < 1e-6, f"Row {i + 1} score mismatch."
        assert int(class_label) == expected_row[4], f"Row {i + 1} class_label mismatch."

def test_validation_errors_txt():
    file_path = "/home/user/validation_errors.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_errors = ["2", "3", "4", "5"]
    assert lines == expected_errors, f"validation_errors.txt content mismatch. Expected {expected_errors}, got {lines}."