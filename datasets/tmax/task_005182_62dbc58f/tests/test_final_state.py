# test_final_state.py

import os
import csv
import pytest

def test_profile_sh_exists_and_executable():
    script_path = "/home/user/profile.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_results_csv_content():
    results_path = "/home/user/results.csv"
    assert os.path.exists(results_path), f"The results file {results_path} does not exist."

    expected_data = [
        {"Threads": "1", "ActualTime": "100.0000", "IdealTime": "100.0000", "Efficiency": "1.0000"},
        {"Threads": "2", "ActualTime": "52.0000", "IdealTime": "50.0000", "Efficiency": "0.9615"},
        {"Threads": "4", "ActualTime": "31.0000", "IdealTime": "25.0000", "Efficiency": "0.8065"},
        {"Threads": "8", "ActualTime": "26.5000", "IdealTime": "12.5000", "Efficiency": "0.4717"},
    ]

    with open(results_path, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["Threads", "ActualTime", "IdealTime", "Efficiency"], \
            "The header of results.csv is incorrect or missing."

        rows = list(reader)
        assert len(rows) == 4, f"Expected 4 rows of data in results.csv, found {len(rows)}."

        for i, expected_row in enumerate(expected_data):
            for key in expected_row:
                actual_val = rows[i].get(key, "").strip()
                expected_val = expected_row[key]
                assert actual_val == expected_val, \
                    f"Row {i+1} mismatch for {key}: expected {expected_val}, got {actual_val}."

def test_mse_txt_content():
    mse_path = "/home/user/mse.txt"
    assert os.path.exists(mse_path), f"The MSE file {mse_path} does not exist."

    with open(mse_path, 'r') as f:
        content = f.read().strip()

    assert content == "59.0000", f"Expected MSE to be '59.0000', got '{content}'."