# test_final_state.py

import os
import re
import pytest

def test_cpp_file_contains_recursive_cte():
    cpp_path = "/home/user/db_traversal.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."

    with open(cpp_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert re.search(r'WITH\s+RECURSIVE', content, re.IGNORECASE), "The C++ file does not contain a 'WITH RECURSIVE' CTE query."

def test_executable_exists():
    exe_path = "/home/user/db_traversal"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing. Did you compile the program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_log_file_content():
    log_path = "/home/user/optimized_paths.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did you run the executable?"

    expected_lines = [
        "Node: Service_B, Shortest Depth: 1",
        "Node: Service_C, Shortest Depth: 1",
        "Node: Service_D, Shortest Depth: 2",
        "Node: Service_E, Shortest Depth: 3",
        "Node: Service_F, Shortest Depth: 2",
        "Node: Service_G, Shortest Depth: 4"
    ]

    with open(log_path, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Log file content does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )