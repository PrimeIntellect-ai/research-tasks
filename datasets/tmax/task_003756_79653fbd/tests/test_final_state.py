# test_final_state.py

import os
import csv
import pytest

def test_optimized_paths_csv_exists():
    file_path = "/home/user/results/optimized_paths.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

def test_optimized_paths_csv_content():
    file_path = "/home/user/results/optimized_paths.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

    expected_rows = [
        {"query_id": "q1", "path": "A->C->B->D->E", "total_cost": "12", "total_delay": "11"},
        {"query_id": "q2", "path": "A->C->B->D->E->F", "total_cost": "13", "total_delay": "21"},
        {"query_id": "q3", "path": "C->B->D", "total_cost": "8", "total_delay": "6"},
    ]

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)

        # Check header
        expected_fields = ["query_id", "path", "total_cost", "total_delay"]
        assert reader.fieldnames is not None, "CSV file is empty or missing headers."
        assert [f.strip() for f in reader.fieldnames] == expected_fields, \
            f"CSV headers do not match. Expected {expected_fields}, got {reader.fieldnames}"

        rows = list(reader)
        assert len(rows) == len(expected_rows), \
            f"Expected {len(expected_rows)} rows of data, but found {len(rows)}."

        for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
            actual_clean = {k.strip(): v.strip() for k, v in actual.items()}
            assert actual_clean == expected, \
                f"Row {i + 1} does not match expected output.\nExpected: {expected}\nActual: {actual_clean}"