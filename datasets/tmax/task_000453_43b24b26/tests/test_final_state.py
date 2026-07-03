# test_final_state.py
import os
import csv

def test_error_summary_exists():
    file_path = "/home/user/error_summary.csv"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_error_summary_content():
    file_path = "/home/user/error_summary.csv"

    expected_rows = [
        ["server", "Auth_Failure", "DB_Timeout", "OOM"],
        ["srv-A", "1", "0", "1"],
        ["srv-B", "0", "1", "0"],
        ["srv-C", "0", "0", "1"]
    ]

    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            actual_rows = list(reader)
    except UnicodeDecodeError:
        assert False, f"The file {file_path} is not properly encoded in UTF-8."
    except Exception as e:
        assert False, f"Failed to read {file_path}: {e}"

    assert actual_rows == expected_rows, (
        f"The content of {file_path} does not match the expected output.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )