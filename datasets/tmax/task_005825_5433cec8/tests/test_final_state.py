# test_final_state.py
import os
import csv

def test_c_source_file_exists():
    assert os.path.exists('/home/user/process.c'), "/home/user/process.c does not exist."
    assert os.path.isfile('/home/user/process.c'), "/home/user/process.c is not a file."

def test_c_executable_exists():
    assert os.path.exists('/home/user/process'), "/home/user/process executable does not exist."
    assert os.path.isfile('/home/user/process'), "/home/user/process is not a file."
    assert os.access('/home/user/process', os.X_OK), "/home/user/process is not executable."

def test_output_csv_exists():
    assert os.path.exists('/home/user/output.csv'), "/home/user/output.csv does not exist."
    assert os.path.isfile('/home/user/output.csv'), "/home/user/output.csv is not a file."

def test_output_csv_content_and_encoding():
    # Read the file using UTF-8 encoding
    try:
        with open('/home/user/output.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except UnicodeDecodeError:
        assert False, "/home/user/output.csv is not valid UTF-8."
    except Exception as e:
        assert False, f"Failed to read /home/user/output.csv: {e}"

    expected_rows = [
        ["ID", "Department", "Feedback"],
        ["1", "Sales", "Great work"],
        ["2", "Engineering", "Needs\nimprovement"],
        ["3", "Sales", "Café is nice"],
        ["5", "Engineering", "Good"]
    ]

    assert rows == expected_rows, f"The content of /home/user/output.csv is incorrect. Expected {expected_rows}, but got {rows}."