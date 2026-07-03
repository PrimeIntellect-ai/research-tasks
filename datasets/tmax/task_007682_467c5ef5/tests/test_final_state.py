# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    """Verify that the C source file exists."""
    source_path = "/home/user/route_solver.c"
    assert os.path.exists(source_path), f"C source file {source_path} is missing."
    assert os.path.isfile(source_path), f"Path {source_path} exists but is not a file."

def test_executable_exists():
    """Verify that the compiled executable exists."""
    exe_path = "/home/user/route_solver"
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing."
    assert os.path.isfile(exe_path), f"Path {exe_path} exists but is not a file."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_log_file_content():
    """Verify that the shortest_path.log file contains the correct output."""
    log_path = "/home/user/shortest_path.log"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(log_path), f"Path {log_path} exists but is not a file."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "Shortest Transit Time: 30\n"
        "Route: Seattle -> Denver -> Chicago -> NewYork -> Miami"
    )

    # Normalize line endings and strip trailing/leading whitespaces
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines()]

    assert actual_lines == expected_lines, (
        f"Log file content does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{content}"
    )