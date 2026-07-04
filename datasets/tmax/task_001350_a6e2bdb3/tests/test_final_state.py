# test_final_state.py

import os
import pytest

def test_analyze_sh_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_results_csv_content():
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"The results file {results_path} does not exist."

    expected_content = (
        "spring_id,k,num_samples\n"
        "A,19.86,3\n"
        "B,80.00,3\n"
        "C,50.00,3"
    )

    with open(results_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The contents of {results_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_stiff_springs_txt_content():
    stiff_path = "/home/user/stiff_springs.txt"
    assert os.path.isfile(stiff_path), f"The file {stiff_path} does not exist."

    expected_content = "B"

    with open(stiff_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The contents of {stiff_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )