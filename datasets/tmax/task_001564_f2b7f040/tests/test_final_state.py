# test_final_state.py

import os
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/clean_data.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cleaned_data():
    cleaned_data_path = "/home/user/cleaned_data.csv"
    assert os.path.exists(cleaned_data_path), f"Cleaned data file {cleaned_data_path} does not exist."

    expected_content = """id,age,income,score
1,25,50000,0.8
4,30,75000,0.7
6,50,120000,0.85
8,35,80000,0.95
9,28,90000,0.88"""

    with open(cleaned_data_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {cleaned_data_path} does not match the expected cleaned dataset."

def test_experiment_log():
    log_path = "/home/user/experiment_log.txt"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.readlines()

    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Initial: 10 rows, Cleaned: 5 rows$")

    match_found = any(pattern.match(line.strip()) for line in lines)
    assert match_found, f"No line in {log_path} matches the expected log format and counts."