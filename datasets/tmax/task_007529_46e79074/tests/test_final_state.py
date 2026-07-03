# test_final_state.py

import os
import re
import pytest

def test_critical_path_output():
    """Verify that the critical path output file exists and contains the correct value."""
    output_path = "/home/user/critical_path.txt"
    assert os.path.exists(output_path), f"Output file not found at {output_path}"
    assert os.path.isfile(output_path), f"{output_path} is not a regular file"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "MAX_LATENCY: 75", f"Expected 'MAX_LATENCY: 75', but got '{content}'"

def test_analyzer_cpp_exists_and_contains_cte():
    """Verify that the C++ source file exists and contains a recursive CTE."""
    cpp_path = "/home/user/analyzer.cpp"
    assert os.path.exists(cpp_path), f"C++ source file not found at {cpp_path}"
    assert os.path.isfile(cpp_path), f"{cpp_path} is not a regular file"

    with open(cpp_path, "r") as f:
        content = f.read()

    # Check for WITH RECURSIVE (case-insensitive)
    assert re.search(r"WITH\s+RECURSIVE", content, re.IGNORECASE), "C++ source code does not contain a recursive CTE (WITH RECURSIVE)"

def test_analyzer_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_path = "/home/user/analyzer"
    assert os.path.exists(exe_path), f"Compiled executable not found at {exe_path}"
    assert os.path.isfile(exe_path), f"{exe_path} is not a regular file"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable"