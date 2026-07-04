# test_final_state.py
import os

def test_source_file_exists():
    path = "/home/user/etl.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_executable_exists():
    path = "/home/user/etl"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_csv_content():
    path = "/home/user/output.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    expected_content = """timestamp,sensor,value
2023-01-01T12:00:00Z,alpha,10.0
2023-01-01T12:00:00Z,beta,12.0
2023-01-01T12:01:00Z,alpha,10.0
2023-01-01T12:01:00Z,beta,12.0
2023-01-01T12:02:00Z,alpha,10.5
2023-01-01T12:02:00Z,beta,12.5
2023-01-01T12:03:00Z,alpha,10.5
2023-01-01T12:03:00Z,beta,12.5
2023-01-01T12:04:00Z,alpha,10.5
2023-01-01T12:04:00Z,beta,12.5
2023-01-01T12:05:00Z,alpha,11.2
2023-01-01T12:05:00Z,beta,13.0
"""

    with open(path, 'r', encoding='utf-8') as f:
        actual_content = f.read()

    # Normalize line endings and strip trailing whitespace
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, f"Content of {path} does not match the expected output."