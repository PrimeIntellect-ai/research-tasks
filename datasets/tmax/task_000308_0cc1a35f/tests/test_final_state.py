# test_final_state.py

import os
import json
import csv
import subprocess
import pytest

def test_processed_data_csv():
    file_path = "/home/user/processed_data.csv"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{file_path} is empty."
    header = rows[0]
    assert header == ["timestamp", "feature_alpha", "feature_beta"], f"Incorrect header in {file_path}: {header}"

    # Check data sorting and values
    expected_data = [
        ["1", "0.0", "5.0"],
        ["2", "1.0", "3.03265"],
        ["3", "2.0", "1.8394"],
        ["4", "3.0", "1.11565"],
        ["5", "4.0", "0.67668"],
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, but got {len(data_rows)}."

    for i, expected in enumerate(expected_data):
        # We allow small float formatting differences by parsing as float
        assert float(data_rows[i][0]) == float(expected[0]), f"Row {i+1} timestamp mismatch."
        assert float(data_rows[i][1]) == float(expected[1]), f"Row {i+1} feature_alpha mismatch."
        assert abs(float(data_rows[i][2]) - float(expected[2])) < 1e-4, f"Row {i+1} feature_beta mismatch."

def test_params_json():
    file_path = "/home/user/params.json"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON.")

    assert "A" in params, "Key 'A' missing in params.json."
    assert "B" in params, "Key 'B' missing in params.json."

    # Check values
    assert 4.95 <= params["A"] <= 5.05, f"Value of A ({params['A']}) is outside expected range [4.95, 5.05]."
    assert 0.45 <= params["B"] <= 0.55, f"Value of B ({params['B']}) is outside expected range [0.45, 0.55]."

def test_python_files_exist():
    assert os.path.isfile("/home/user/optimizer.py"), "/home/user/optimizer.py is missing."
    assert os.path.isfile("/home/user/test_optimization.py"), "/home/user/test_optimization.py is missing."

def test_pytest_runs_successfully():
    test_file = "/home/user/test_optimization.py"
    assert os.path.isfile(test_file), f"{test_file} is missing."

    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed on {test_file}. Output:\n{result.stdout}\n{result.stderr}"