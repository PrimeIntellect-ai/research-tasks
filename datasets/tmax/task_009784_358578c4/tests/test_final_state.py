# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = '/home/user/analyze_logs.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_processed_files_exist():
    alpha_csv = '/home/user/processed/server_alpha.csv'
    beta_csv = '/home/user/processed/server_beta.csv'

    assert os.path.isfile(alpha_csv), f"Output file {alpha_csv} does not exist."
    assert os.path.isfile(beta_csv), f"Output file {beta_csv} does not exist."

def test_server_alpha_output():
    alpha_csv = '/home/user/processed/server_alpha.csv'
    expected_lines = [
        "1,2,2",
        "2,5,7",
        "3,0,7",
        "4,3,8"
    ]

    with open(alpha_csv, 'r') as f:
        content = f.read().strip().split('\n')

    assert content == expected_lines, f"Content of {alpha_csv} does not match expected output. Got: {content}"

def test_server_beta_output():
    beta_csv = '/home/user/processed/server_beta.csv'
    expected_lines = [
        "10,10,10",
        "11,5,15"
    ]

    with open(beta_csv, 'r') as f:
        content = f.read().strip().split('\n')

    assert content == expected_lines, f"Content of {beta_csv} does not match expected output. Got: {content}"