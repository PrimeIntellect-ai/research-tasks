# test_final_state.py

import os
import pytest

def test_source_code_exists():
    source_path = "/home/user/graph_tool.c"
    assert os.path.exists(source_path), f"The source code file {source_path} is missing."
    assert os.path.isfile(source_path), f"The path {source_path} is not a file."

def test_executable_exists():
    exec_path = "/home/user/graph_tool"
    assert os.path.exists(exec_path), f"The executable file {exec_path} is missing."
    assert os.path.isfile(exec_path), f"The path {exec_path} is not a file."
    assert os.access(exec_path, os.X_OK), f"The file {exec_path} is not executable."

def test_page2_csv_contents():
    output_path = "/home/user/page2.csv"
    assert os.path.exists(output_path), f"The output file {output_path} is missing."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

    expected_content = """node,depth
K,2
L,2
M,3
N,3
O,3
P,3
Q,3
R,3
S,3
T,3"""

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    # Normalize line endings
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {output_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )