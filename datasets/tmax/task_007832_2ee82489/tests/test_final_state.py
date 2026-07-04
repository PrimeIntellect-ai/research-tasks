# test_final_state.py

import os
import csv

def test_highly_active_mutuals_csv_exists_and_correct():
    """Verify that the output CSV file exists and contains the correct results."""
    output_path = "/home/user/highly_active_mutuals.csv"

    assert os.path.isfile(output_path), f"Expected output file not found at {output_path}"

    with open(output_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]  # ignore empty lines

    expected_rows = [
        ["userA", "userB", "clicksA", "clicksB"],
        ["u1", "u2", "4", "3"],
        ["u1", "u4", "4", "3"]
    ]

    assert len(rows) > 0, "The CSV file is empty."
    assert rows[0] == expected_rows[0], f"CSV header is incorrect. Expected {expected_rows[0]}, got {rows[0]}"

    # Sort actual data rows to be robust against ordering differences if the student didn't sort,
    # but the prompt says "Sort the CSV output by userA ascending, then userB ascending."
    # So we should enforce the exact order.
    assert rows == expected_rows, f"CSV contents do not match the expected output. Expected {expected_rows}, got {rows}"