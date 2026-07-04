# test_final_state.py

import os
import pytest

def test_extracted_data_dir():
    extract_dir = "/home/user/extracted_data"
    assert os.path.exists(extract_dir), f"Directory {extract_dir} does not exist."
    assert os.path.isdir(extract_dir), f"{extract_dir} should be a directory."

    expected_files = {"chunk1.tar.gz", "chunk2.tar.gz", "chunk3.tar.gz"}
    actual_files = set(os.listdir(extract_dir))
    for expected in expected_files:
        assert expected in actual_files, f"Expected {expected} to be extracted to {extract_dir}."

def test_aggregator_script():
    script_path = "/home/user/aggregator.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} should be a file."

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, "The script must use fcntl.flock to acquire an exclusive lock."

def test_results_csv():
    results_path = "/home/user/results.csv"
    assert os.path.exists(results_path), f"Results file {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} should be a file."

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "alpha,60.0",
        "beta,31.0",
        "gamma,50.0"
    }

    assert set(lines) == expected_lines, f"Expected {expected_lines} in {results_path}, but got {set(lines)}."
    assert len(lines) == 3, f"Expected exactly 3 lines in {results_path}, but got {len(lines)}."