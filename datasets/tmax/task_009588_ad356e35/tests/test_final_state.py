# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = '/home/user/prepare_data.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_training_set_exists():
    output_path = '/home/user/data/training_set.csv'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_training_set_content():
    output_path = '/home/user/data/training_set.csv'

    expected_lines = [
        "id,f1,f2,y",
        "4,10,1,89",
        "5,7,0,35",
        "2,5,5,26",
        "3,2,8,14",
        "1,4,2,8"
    ]

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {output_path} is incorrect. Expected {expected_lines}, got {actual_lines}"