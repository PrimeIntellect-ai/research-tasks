# test_final_state.py
import os
import pytest

def test_script_exists():
    script_path = "/home/user/build_dataset.sh"
    assert os.path.isfile(script_path), f"The bash script {script_path} does not exist."

def test_output_directory_exists():
    dir_path = "/home/user/processed"
    assert os.path.isdir(dir_path), f"The output directory {dir_path} does not exist."

def test_dataset_csv_content():
    csv_path = "/home/user/processed/dataset.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} does not exist."

    expected_lines = [
        "uid,age,country,tokenized_review",
        "101,25,US,this-is-awesome",
        "104,40,FR,works-well-but-a-bit-pricey",
        "108,29,JP,100-perfect"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines[0] == expected_lines[0], f"Expected header '{expected_lines[0]}', but got '{actual_lines[0]}'."

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, but got {len(actual_lines)}."

    for i in range(1, len(expected_lines)):
        assert actual_lines[i] == expected_lines[i], f"Expected row {i} to be '{expected_lines[i]}', but got '{actual_lines[i]}'."