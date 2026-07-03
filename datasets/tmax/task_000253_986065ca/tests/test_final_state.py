# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    """Test that the detect_cycle.sh script exists and is executable."""
    script_path = "/home/user/detect_cycle.sh"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_deadlock_report_exists():
    """Test that the deadlock_report.txt file exists."""
    report_path = "/home/user/deadlock_report.txt"
    assert os.path.isfile(report_path), f"Report file not found: {report_path}"

def test_deadlock_report_content():
    """Test that the deadlock_report.txt contains the correct cycle."""
    report_path = "/home/user/deadlock_report.txt"

    if not os.path.isfile(report_path):
        pytest.fail(f"Cannot check content, file missing: {report_path}")

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_cycle = "TX_994 -> TX_772 -> TX_881 -> TX_994"
    assert content == expected_cycle, f"Expected report content to be '{expected_cycle}', but got '{content}'"