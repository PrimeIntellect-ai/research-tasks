# test_final_state.py

import os
import pytest
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/run_analysis.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cleaned_dataset():
    cleaned_path = "/home/user/cleaned_dataset.csv"
    assert os.path.isfile(cleaned_path), f"Cleaned dataset {cleaned_path} does not exist."

    with open(cleaned_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 5, f"Expected 5 rows (including header) in {cleaned_path}, found {len(rows)}."
    assert rows[0] == ["record_id", "measurement", "notes"], "Header is incorrect or missing."

    # Check that invalid rows are removed and valid rows are kept
    record_ids = [row[0] for row in rows[1:]]
    assert "2" not in record_ids, "Row with NaN measurement was not removed."
    assert "3" not in record_ids, "Row with measurement > 100 was not removed."
    assert "5" not in record_ids, "Row with measurement < 0 was not removed."

    expected_ids = {"1", "4", "6", "7"}
    assert set(record_ids) == expected_ids, f"Expected record IDs {expected_ids}, found {set(record_ids)}."

def test_ci_output():
    ci_path = "/home/user/ci.txt"
    assert os.path.isfile(ci_path), f"Confidence interval file {ci_path} does not exist."

    with open(ci_path, "r") as f:
        content = f.read().strip()

    assert "44.55,46.45" in content, f"Expected CI '44.55,46.45' in {ci_path}, but got '{content}'."

def test_retrieved_id():
    id_path = "/home/user/retrieved_id.txt"
    assert os.path.isfile(id_path), f"Retrieved ID file {id_path} does not exist."

    with open(id_path, "r") as f:
        content = f.read().strip()

    assert content == "4", f"Expected retrieved ID '4', but got '{content}'."