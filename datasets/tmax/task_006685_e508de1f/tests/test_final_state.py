# test_final_state.py

import os
import re
import pytest

def test_extrusion_report():
    """Test that the extrusion_report.txt exists and contains the correct sum."""
    report_path = "/home/user/extrusion_report.txt"
    assert os.path.exists(report_path), f"File {report_path} is missing."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "4.25", f"Expected extrusion_report.txt to contain '4.25', but got '{content}'."

def test_analyzer_c_code():
    """Test that analyzer.c exists and contains required flock calls."""
    source_path = "/home/user/analyzer.c"
    assert os.path.exists(source_path), f"File {source_path} is missing."
    assert os.path.isfile(source_path), f"{source_path} is not a file."

    with open(source_path, "r") as f:
        content = f.read()

    assert "flock" in content, "The source code does not contain a call to 'flock'."
    assert "LOCK_SH" in content, "The source code does not use 'LOCK_SH' for shared locking."

def test_analyzer_executable():
    """Test that the analyzer executable was compiled."""
    exec_path = "/home/user/analyzer"
    assert os.path.exists(exec_path), f"Executable {exec_path} is missing. Did you compile the C program?"
    assert os.path.isfile(exec_path), f"{exec_path} is not a file."
    assert os.access(exec_path, os.X_OK), f"File {exec_path} is not executable."