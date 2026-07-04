# test_final_state.py

import os
import pytest

def test_validator_executable_exists():
    executable_path = "/home/user/validator"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_dag_step_script_exists():
    script_path = "/home/user/dag_step.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."

def test_clean_import_csv():
    file_path = "/home/user/clean_import.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist. Did you run your script?"

    expected_valid = [
        "1,Alice,30,alice@example.com",
        "5,Eve,120,eve@example.com",
        "7,Grace,18,grace@example.com"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_valid, "The contents of clean_import.csv do not match the expected valid records."

def test_rejected_csv():
    file_path = "/home/user/rejected.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist. Did you run your script?"

    expected_rejected = [
        "2,Bob,17,bob@example.com",
        "-3,Charlie,25,charlie@example.com",
        "4,David,45,david.example.com",
        "6,Frank,121,frank@example.com",
        "invalid,Hank,40,hank@example.com",
        "9,Ivy,bad,ivy@example.com"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_rejected, "The contents of rejected.csv do not match the expected rejected records."