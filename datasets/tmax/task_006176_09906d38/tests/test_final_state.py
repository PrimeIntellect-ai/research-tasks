# test_final_state.py
import os
import gzip
import pytest

def test_critical_logs_file_exists():
    output_file = "/home/user/critical_logs.gz"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Output path {output_file} is not a file."

def test_critical_logs_content():
    output_file = "/home/user/critical_logs.gz"

    expected_lines = [
        "3|2023-10-01T10:02:00|FATAL|Kernel panic\n",
        "5|2023-10-01T10:05:00|ERROR|Disk full\n",
        "7|2023-10-01T10:07:00|ERROR|Network down\n",
        "8|2023-10-01T10:08:00|FATAL|OOM\n"
    ]

    try:
        with gzip.open(output_file, 'rt') as f:
            actual_lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Failed to read {output_file} as a gzip text file: {e}")

    assert actual_lines == expected_lines, (
        f"The contents of {output_file} do not match the expected output. "
        f"Expected {len(expected_lines)} specific lines, but got {len(actual_lines)} lines. "
        f"Actual content: {actual_lines}"
    )