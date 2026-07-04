# test_final_state.py

import os

def test_c_source_exists():
    path = "/home/user/process_logs.c"
    assert os.path.exists(path), f"C source file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_compiled_binary_exists():
    path = "/home/user/process_logs"
    assert os.path.exists(path), f"Compiled binary {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_rolling_stats_csv_content():
    path = "/home/user/rolling_stats.csv"
    assert os.path.exists(path), f"Output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    expected_content = """2023-10-12 10:00:00,100.00
2023-10-12 10:00:02,125.00
2023-10-12 10:00:05,100.00
2023-10-12 10:00:07,133.33
2023-10-12 10:00:08,166.67"""

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {path} does not match expected output.\nExpected:\n{expected_content}\n\nGot:\n{content}"