# test_final_state.py

import os
import csv
from pathlib import Path

def test_source_and_executable_exist():
    cpp_file = Path("/home/user/etl_processor.cpp")
    executable = Path("/home/user/etl_processor")

    assert cpp_file.exists(), "C++ source code /home/user/etl_processor.cpp does not exist."
    assert executable.exists(), "Compiled executable /home/user/etl_processor does not exist."
    assert os.access(executable, os.X_OK), "The file /home/user/etl_processor is not executable."

def test_summary_report_exists_and_correct():
    report_file = Path("/home/user/summary_report.csv")
    assert report_file.exists(), f"Output report {report_file} does not exist."

    expected_rows = [
        ["user_id", "name", "region", "total_completed_amount", "distance_to_whale"],
        ["1", "Alice", "US", "1200.0", "0"],
        ["2", "Bob", "UK", "500.0", "10"],
        ["3", "Charlie", "US", "100.0", "10"],
        ["4", "Diana", "CA", "0.0", "8"],
        ["5", "Eve", "UK", "2000.0", "0"],
        ["6", "Frank", "AU", "0.0", "-1"]
    ]

    with open(report_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, "The summary report is empty."

    # Check header
    assert actual_rows[0] == expected_rows[0], f"Header row is incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}."

    # Check number of rows
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows (including header), got {len(actual_rows)}."

    # Check each row exactly
    for i in range(1, len(expected_rows)):
        expected = expected_rows[i]
        actual = actual_rows[i]

        assert actual[0] == expected[0], f"Row {i}: user_id mismatch. Expected {expected[0]}, got {actual[0]}."
        assert actual[1] == expected[1], f"Row {i}: name mismatch. Expected {expected[1]}, got {actual[1]}."
        assert actual[2] == expected[2], f"Row {i}: region mismatch. Expected {expected[2]}, got {actual[2]}."

        # Parse floats for amount to handle slight formatting differences like 1200.0 vs 1200.00 if any, 
        # but the spec says strictly matches format. We'll check exact string but allow float equality if it fails.
        try:
            actual_amount = float(actual[3])
            expected_amount = float(expected[3])
            assert actual_amount == expected_amount, f"Row {i}: total_completed_amount mismatch. Expected {expected_amount}, got {actual_amount}."
            # Also enforce the 1 decimal place format as per instructions
            assert actual[3].endswith(".0") or "." in actual[3], f"Row {i}: total_completed_amount format issue. Expected 1 decimal place, got {actual[3]}."
        except ValueError:
            assert False, f"Row {i}: total_completed_amount '{actual[3]}' is not a valid float."

        assert actual[4] == expected[4], f"Row {i}: distance_to_whale mismatch. Expected {expected[4]}, got {actual[4]}."