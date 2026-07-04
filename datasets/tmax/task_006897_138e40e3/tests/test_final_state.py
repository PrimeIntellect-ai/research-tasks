# test_final_state.py

import os
import re
import pytest

def test_executable_exists():
    """Test that the evaluate executable was compiled."""
    exe_path = "/home/user/evaluate"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you compile the script?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_report_exists():
    """Test that report.txt was successfully created."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"File {report_path} was not created. Did you fix the file writing bug and run the executable?"

def test_report_content():
    """Test that report.txt contains the correct results."""
    report_path = "/home/user/report.txt"
    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {report_path} is empty."

    # Check for Best Threshold
    threshold_match = re.search(r"Best Threshold:\s*0\.1", content)
    assert threshold_match, f"Could not find 'Best Threshold: 0.1' in {report_path}. Found:\n{content}"

    # Check for Accuracy
    accuracy_match = re.search(r"Accuracy:\s*1(\.0*)?", content)
    assert accuracy_match, f"Could not find 'Accuracy: 1' (or 1.0) in {report_path}. Found:\n{content}"