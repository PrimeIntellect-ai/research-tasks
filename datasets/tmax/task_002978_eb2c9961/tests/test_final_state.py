# test_final_state.py
import os
import csv
import pytest

def test_csv_exists():
    csv_path = '/home/user/circular_flows.csv'
    assert os.path.isfile(csv_path), f"Output CSV file {csv_path} does not exist."

def test_csv_content():
    csv_path = '/home/user/circular_flows.csv'
    assert os.path.isfile(csv_path), f"Output CSV file {csv_path} does not exist."

    expected_headers = ['acct_A', 'acct_B', 'acct_C', 'cycle_total', 'risk_rank']
    expected_rows = [
        ['Xavier', 'Yolanda', 'Zack', 15000.0, '1'],
        ['Alice', 'Bob', 'Charlie', 4500.0, '2']
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        assert headers == expected_headers, f"Expected headers {expected_headers}, but got {headers}."

        rows = list(reader)
        assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(rows)}."

        for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
            assert len(actual) == 5, f"Row {i+1} has {len(actual)} columns, expected 5."

            # Check accounts
            assert actual[:3] == expected[:3], f"Row {i+1} accounts mismatch: expected {expected[:3]}, got {actual[:3]}"

            # Check cycle_total (allow for float representation differences)
            try:
                actual_total = float(actual[3])
            except ValueError:
                pytest.fail(f"Row {i+1} cycle_total '{actual[3]}' is not a valid float.")
            assert actual_total == expected[3], f"Row {i+1} cycle_total mismatch: expected {expected[3]}, got {actual_total}"

            # Check risk_rank
            assert actual[4] == expected[4], f"Row {i+1} risk_rank mismatch: expected '{expected[4]}', got '{actual[4]}'"