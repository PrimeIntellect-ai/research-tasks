# test_final_state.py
import os
import gzip
import pytest

def test_summary_file_exists():
    path = '/home/user/summary.csv.gz'
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

def test_summary_file_size_threshold():
    path = '/home/user/summary.csv.gz'
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    file_size = os.path.getsize(path)
    threshold = 250
    assert file_size < threshold, f"File size of {path} is {file_size} bytes, which is not less than the threshold of {threshold} bytes."

def test_summary_file_content():
    path = '/home/user/summary.csv.gz'
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    try:
        with gzip.open(path, 'rt') as f:
            content = f.read().strip()
    except Exception as e:
        pytest.fail(f"Failed to read {path} as a gzip file: {e}")

    expected_lines = [
        "D001,API",
        "D002,Guide",
        "D003,API",
        "D004,FAQ",
        "D005,Guide"
    ]

    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Content of {path} does not match the expected CSV format and data. Got: {actual_lines}"