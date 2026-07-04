# test_final_state.py

import os
import pytest

def test_missing_config_path_file():
    path_file = "/home/user/missing_config_path.txt"
    assert os.path.isfile(path_file), f"The file {path_file} was not created."

    with open(path_file, "r") as f:
        content = f.read().strip()

    expected_path = "/home/user/pipeline/.hidden_conf/rules.ini"
    assert content == expected_path, f"Expected {path_file} to contain '{expected_path}', but found '{content}'."

def test_config_file_created():
    config_file = "/home/user/pipeline/.hidden_conf/rules.ini"
    assert os.path.isfile(config_file), f"The missing configuration file {config_file} was not created."

def test_summary_csv_content():
    summary_file = "/home/user/pipeline/summary.csv"
    assert os.path.isfile(summary_file), f"The final report {summary_file} was not generated."

    expected_lines = [
        "2023-10-01,SUCCESS",
        "2023-10-01,RETRY",
        "2023-10-01,FAILURE",
        "2023-10-02,SUCCESS"
    ]

    with open(summary_file, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"The content of {summary_file} is incorrect. Expected: {expected_lines}, but got: {actual_lines}"