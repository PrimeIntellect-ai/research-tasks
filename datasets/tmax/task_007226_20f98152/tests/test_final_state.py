# test_final_state.py
import os
import re
import pytest

def test_clean_data_csv():
    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_data_path), f"The clean data file is missing at {clean_data_path}"

    with open(clean_data_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected exactly 50 lines in {clean_data_path}, but found {len(lines)}."

    # Check format X,Y
    for i, line in enumerate(lines):
        match = re.match(r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$', line)
        assert match is not None, f"Line {i+1} in {clean_data_path} is not in the correct format 'X,Y': {line}"

def test_tune_executable_exists():
    tune_path = "/home/user/tune"
    assert os.path.isfile(tune_path), f"The compiled executable is missing at {tune_path}"
    assert os.access(tune_path, os.X_OK), f"The file at {tune_path} is not executable."

def test_best_lambda_output():
    best_lambda_path = "/home/user/best_lambda.txt"
    assert os.path.isfile(best_lambda_path), f"The output file is missing at {best_lambda_path}"

    with open(best_lambda_path, 'r') as f:
        content = f.read().strip()

    assert content == "0.1", f"Expected best lambda to be '0.1', but got '{content}'"