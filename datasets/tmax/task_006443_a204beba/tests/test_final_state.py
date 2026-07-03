# test_final_state.py
import os
import pytest

def test_directories_created():
    expected_dirs = [
        '/home/user/accepted',
        '/home/user/rejected',
        '/home/user/output',
        '/home/user/logs'
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Directory {d} was not created."

def test_accepted_files():
    accepted_dir = '/home/user/accepted'
    expected_files = {'data1.csv', 'data3.csv'}

    assert os.path.isdir(accepted_dir), f"{accepted_dir} does not exist."
    actual_files = set(os.listdir(accepted_dir))

    for f in expected_files:
        assert f in actual_files, f"Expected {f} to be in {accepted_dir}, but it was not."

def test_rejected_files():
    rejected_dir = '/home/user/rejected'
    expected_files = {'data2.csv', 'data4.csv'}

    assert os.path.isdir(rejected_dir), f"{rejected_dir} does not exist."
    actual_files = set(os.listdir(rejected_dir))

    for f in expected_files:
        assert f in actual_files, f"Expected {f} to be in {rejected_dir}, but it was not."

def test_consolidated_csv_content():
    output_file = '/home/user/output/consolidated.csv'
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_lines = [
        "A1B2C,User logged in successfully.",
        "P0O9I,Query execution took 45ms.",
        "Q1W2E,Database connection lost! Retry in 5s...",
        "X9Y8Z,Failed to load module auth."
    ]

    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {output_file} do not match expected output. "
        f"Expected:\n{expected_lines}\nGot:\n{actual_lines}"
    )

def test_pipeline_log_content():
    log_file = '/home/user/logs/pipeline.log'
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, 'r') as f:
        content = f.read()

    assert "START: Validation" in content, f"'START: Validation' missing from {log_file}"
    assert "START: Cleaning" in content, f"'START: Cleaning' missing from {log_file}"
    assert "END: Pipeline complete" in content, f"'END: Pipeline complete' missing from {log_file}"

    # Check ordering
    idx1 = content.find("START: Validation")
    idx2 = content.find("START: Cleaning")
    idx3 = content.find("END: Pipeline complete")

    assert idx1 < idx2 < idx3, "Log messages are not in the correct order."