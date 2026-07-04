# test_final_state.py

import os
import pytest

def test_raw_configs_directory_exists_and_populated():
    """Test that the raw_configs directory exists and contains the extracted csv files."""
    dir_path = "/home/user/raw_configs"
    assert os.path.exists(dir_path), f"Directory {dir_path} does not exist. Did you extract the tarball?"
    assert os.path.isdir(dir_path), f"Path {dir_path} is not a directory."

    expected_files = ["server1.csv", "server2.csv", "server3.csv"]
    for f in expected_files:
        file_path = os.path.join(dir_path, f)
        assert os.path.exists(file_path), f"File {f} was not found in {dir_path}."

def test_csv_files_are_utf8():
    """Test that all csv files in raw_configs are UTF-8 encoded."""
    dir_path = "/home/user/raw_configs"
    csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    assert len(csv_files) > 0, "No .csv files found in raw_configs."

    for f in csv_files:
        file_path = os.path.join(dir_path, f)
        try:
            with open(file_path, 'r', encoding='utf-8') as f_obj:
                f_obj.read()
        except UnicodeDecodeError:
            pytest.fail(f"File {f} is not properly UTF-8 encoded.")

def test_rejected_changes_output():
    """Test that rejected_changes.txt contains the correct output."""
    output_file = "/home/user/rejected_changes.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    expected_lines = [
        "srv1:c002",
        "srv2:c102",
        "srv2:c103",
        "srv3:c201"
    ]

    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {output_file} does not match expected output. Got: {content}"