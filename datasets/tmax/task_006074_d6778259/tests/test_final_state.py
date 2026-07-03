# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/collatz_ext"
REPORT_PATH = os.path.join(PROJECT_DIR, "fix_report.txt")
LIB_PATH = os.path.join(PROJECT_DIR, "libcollatz.so")

def test_fix_report_exists():
    """Check that the fix_report.txt file exists."""
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

def test_fix_report_content():
    """Check that the fix_report.txt contains the correct output."""
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Report file {REPORT_PATH} does not contain enough lines. Found {len(lines)}."
    assert lines[0] == "SUCCESS", f"Expected first line to be 'SUCCESS', but got '{lines[0]}'."
    assert lines[1] == "111", f"Expected second line to be '111' (the Collatz sequence length for n=27), but got '{lines[1]}'."

def test_shared_library_exists():
    """Check that the shared library was built."""
    assert os.path.exists(LIB_PATH), f"Shared library {LIB_PATH} was not found. The Makefile might not be properly fixed or executed."

def test_makefile_fixed():
    """Check that the Makefile was modified to include shared library flags."""
    makefile_path = os.path.join(PROJECT_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} does not exist."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-shared" in content, "Makefile does not contain the '-shared' flag required for building a shared library."
    assert "-fPIC" in content, "Makefile does not contain the '-fPIC' flag required for Position Independent Code."