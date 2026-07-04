# test_final_state.py

import os
import csv
import pytest

def test_shared_library_compiled():
    path = "/home/user/libmath.so"
    assert os.path.isfile(path), f"Shared library {path} is missing. Did you compile it?"

def test_orchestrate_script_exists_and_executable():
    path = "/home/user/orchestrate.sh"
    assert os.path.isfile(path), f"Orchestration script {path} is missing."
    assert os.access(path, os.X_OK), f"Orchestration script {path} is not executable."

def test_summary_csv_content():
    path = "/home/user/summary.csv"
    assert os.path.isfile(path), f"Summary CSV {path} is missing."

    expected_rows = [
        ["steps", "file_count"],
        ["7", "1"],
        ["9", "1"],
        ["17", "3"],
        ["19", "2"],
        ["111", "1"],
        ["118", "1"],
        ["178", "1"]
    ]

    actual_rows = []
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert actual_rows == expected_rows, (
        f"CSV content mismatch.\nExpected: {expected_rows}\nActual: {actual_rows}"
    )

def test_organized_data_structure():
    base_dir = "/home/user/organized_data"
    assert os.path.isdir(base_dir), f"Directory {base_dir} is missing."

    expected_structure = {
        "7": ["test_9.json"],
        "9": ["test_5.json"],
        "17": ["test_1.json", "test_6.json", "test_10.json"],
        "19": ["test_3.json", "test_8.json"],
        "111": ["test_2.json"],
        "118": ["test_4.json"],
        "178": ["test_7.json"]
    }

    for steps, files in expected_structure.items():
        step_dir = os.path.join(base_dir, steps)
        assert os.path.isdir(step_dir), f"Directory for {steps} steps ({step_dir}) is missing."

        actual_files = set(os.listdir(step_dir))
        expected_files = set(files)

        assert actual_files == expected_files, (
            f"Mismatch in files for directory {step_dir}.\n"
            f"Expected: {expected_files}\nActual: {actual_files}"
        )

def test_original_test_data_moved():
    path = "/home/user/test_data"
    if os.path.isdir(path):
        # If the directory still exists, it should be empty
        assert len(os.listdir(path)) == 0, f"Original test_data directory {path} is not empty. Files were not moved."