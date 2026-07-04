# test_final_state.py

import os
import hashlib
import pytest

def test_pipeline_script_exists_and_executable():
    path = '/home/user/pipeline.sh'
    assert os.path.exists(path), f"{path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_filter_executable_exists():
    path = '/home/user/filter'
    assert os.path.exists(path), f"Compiled binary {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_cleaned_csv_content():
    path = '/home/user/cleaned.csv'
    assert os.path.exists(path), f"{path} is missing."

    expected_lines = [
        "id,sensor_val,timestamp",
        "1,45.1,1620000001",
        "2,46.2,1620000002",
        "4,44.9,1620000004",
        "6,47.8,1620000006",
        "7,45.5,1620000007",
        "9,37.5,1620000009",
        "10,48.0,1620000010"
    ]

    with open(path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {path} does not match expected filtered output."

def test_checksum_txt_content():
    cleaned_path = '/home/user/cleaned.csv'
    checksum_path = '/home/user/checksum.txt'

    assert os.path.exists(cleaned_path), f"{cleaned_path} is missing."
    assert os.path.exists(checksum_path), f"{checksum_path} is missing."

    with open(cleaned_path, 'rb') as f:
        expected_md5 = hashlib.md5(f.read()).hexdigest()

    with open(checksum_path, 'r') as f:
        checksum_content = f.read().strip()

    assert expected_md5 in checksum_content, f"{checksum_path} does not contain the correct MD5 checksum of {cleaned_path}."

def test_benchmark_txt_content():
    path = '/home/user/benchmark.txt'
    assert os.path.exists(path), f"{path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    assert "real" in content, f"'real' timing missing in {path}."
    assert "user" in content, f"'user' timing missing in {path}."
    assert "sys" in content, f"'sys' timing missing in {path}."