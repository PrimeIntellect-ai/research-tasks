# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Test that the C source code file exists."""
    file_path = "/home/user/decompose.c"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a valid file."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    file_path = "/home/user/decompose"
    assert os.path.exists(file_path), f"The executable {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a valid file."
    assert os.access(file_path, os.X_OK), f"The file {file_path} is not executable."

def test_visualization_content():
    """Test that visualization.txt contains the correct ASCII bar chart."""
    file_path = "/home/user/visualization.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {file_path}, found {len(lines)}."
    assert lines[0] == "Domain 0: **", f"Incorrect output for Domain 0. Got: {lines[0]}"
    assert lines[1] == "Domain 1: **", f"Incorrect output for Domain 1. Got: {lines[1]}"

def test_summary_report_content():
    """Test that decomposition_summary.log contains the correct analysis results."""
    file_path = "/home/user/decomposition_summary.log"
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, found {len(lines)}."
    assert lines[0] == "Cross-domain edges: 2", f"Incorrect cross-domain edge count. Got: {lines[0]}"
    assert lines[1] == "Max degree node in domain 0: 0", f"Incorrect max degree node. Got: {lines[1]}"