# test_final_state.py

import os
import csv
import pytest

def test_etl_script_exists_and_uses_multiprocessing():
    script_path = "/home/user/etl.py"
    assert os.path.isfile(script_path), f"ETL script missing at {script_path}"

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "multiprocessing" in content, "The script does not seem to use the 'multiprocessing' module as required."

def test_output_csv_exists():
    output_path = "/home/user/output/joined_data.csv"
    assert os.path.isfile(output_path), f"Output CSV missing at {output_path}"

def test_output_csv_contents():
    output_path = "/home/user/output/joined_data.csv"
    assert os.path.isfile(output_path), "Cannot test contents, output CSV is missing."

    expected_rows = [
        ["tx_id", "crm_name", "tx_name", "masked_email", "masked_cc"],
        ["TX101", "Jonathon Doe", "Jonathan Doe", "j***@gmail.com", "************4444"],
        ["TX102", "Alice Smith", "Alice Smyth", "a***@yahoo.com", "************8888"]
    ]

    with open(output_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, "The output CSV is empty."
    assert actual_rows[0] == expected_rows[0], f"Expected header {expected_rows[0]}, but got {actual_rows[0]}"

    # Check if the rows match exactly (sorted by tx_id)
    assert actual_rows == expected_rows, f"Expected CSV contents {expected_rows}, but got {actual_rows}"