# test_final_state.py

import os
import pytest

def test_processor_exists():
    assert os.path.isfile('/home/user/processor.c'), "C source code /home/user/processor.c is missing."
    assert os.path.isfile('/home/user/processor'), "Compiled executable /home/user/processor is missing."
    assert os.access('/home/user/processor', os.X_OK), "Compiled executable /home/user/processor is not executable."

def test_features_csv():
    file_path = '/home/user/features.csv'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_lines = {
        "101,6,11",
        "102,6,9",
        "103,5,12",
        "104,4,7",
        "105,6,8",
        "106,4,11",
        "107,3,6"
    }

    with open(file_path, 'r') as f:
        lines = set(line.strip() for line in f if line.strip())

    assert lines == expected_lines, f"Contents of {file_path} do not match the expected feature extraction."

def test_joined_features_csv():
    file_path = '/home/user/joined_features.csv'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_lines = {
        "101,25,US,6,11",
        "102,35,UK,6,9",
        "103,40,CA,5,12",
        "104,22,US,4,7",
        "105,30,AU,6,8",
        "106,45,IN,4,11",
        "107,29,US,3,6"
    }

    with open(file_path, 'r') as f:
        lines = set(line.strip() for line in f if line.strip())

    assert lines == expected_lines, f"Contents of {file_path} do not match the expected joined outputs."

def test_final_sample_csv():
    file_path = '/home/user/final_sample.csv'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_lines = {
        "102,35,UK,6,9",
        "103,40,CA,5,12",
        "105,30,AU,6,8",
        "106,45,IN,4,11"
    }

    with open(file_path, 'r') as f:
        lines = set(line.strip() for line in f if line.strip())

    assert lines == expected_lines, f"Contents of {file_path} do not match the expected filtered outputs (age >= 30)."

def test_experiment_log():
    file_path = '/home/user/experiment_log.txt'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "FINAL_ROWS: 4", f"Contents of {file_path} do not match the expected log output."