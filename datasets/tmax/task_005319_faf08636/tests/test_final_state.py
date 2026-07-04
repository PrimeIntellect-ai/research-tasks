# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/etl_check.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_invalid_ids_content():
    output_path = "/home/user/invalid_ids.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = ["2", "3", "6", "8"]
    assert lines == expected_ids, f"Contents of {output_path} do not match the expected invalid IDs. Expected {expected_ids}, got {lines}."

def test_clean_joined_content():
    output_path = "/home/user/clean_joined.csv"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    expected_content = [
        "id,f1,f2,pred",
        "1,A,10,100",
        "4,D,40,400",
        "5,E,50,-500",
        "7,G,70,700"
    ]

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_content, f"Contents of {output_path} do not match the expected clean joined data."