# test_final_state.py

import os
import pytest

def test_source_file_exists():
    """Check if the C source file exists."""
    assert os.path.exists("/home/user/extract_subgraph.c"), "The C source file /home/user/extract_subgraph.c does not exist."

def test_executable_exists():
    """Check if the compiled executable exists."""
    assert os.path.exists("/home/user/extract_subgraph"), "The executable /home/user/extract_subgraph does not exist."
    assert os.access("/home/user/extract_subgraph", os.X_OK), "The file /home/user/extract_subgraph is not executable."

def test_csv_output():
    """Check if the output CSV exactly matches the expected results."""
    csv_path = "/home/user/out_degrees.csv"
    assert os.path.exists(csv_path), f"The output CSV file {csv_path} does not exist."

    expected_content = """node,out_degree
1,3
3,2
7,2
2,1
4,1
5,1
6,1
8,1
9,0
10,0
11,0
"""

    with open(csv_path, "r") as f:
        actual_content = f.read()

    # Strip trailing whitespace/newlines for a robust comparison
    actual_lines = [line.strip() for line in actual_content.strip().split("\n")]
    expected_lines = [line.strip() for line in expected_content.strip().split("\n")]

    assert actual_lines == expected_lines, f"CSV content does not match expected output.\nExpected:\n{expected_content}\nActual:\n{actual_content}"