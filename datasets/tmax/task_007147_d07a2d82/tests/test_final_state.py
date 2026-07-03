# test_final_state.py

import os
import json
import pytest

def test_audit_c_exists():
    """Check if the C source file exists."""
    c_file_path = "/home/user/audit.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} is missing."

def test_audit_runner_exists_and_executable():
    """Check if the compiled executable exists and is executable."""
    runner_path = "/home/user/audit_runner"
    assert os.path.isfile(runner_path), f"Executable {runner_path} is missing."
    assert os.access(runner_path, os.X_OK), f"File {runner_path} is not executable."

def test_audit_report_contents():
    """Check if the audit report JSON exists and contains the correct values."""
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report {report_path} is missing."

    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "total_3_cycles" in data, "Key 'total_3_cycles' missing in audit report."
    assert "total_cycle_exposure" in data, "Key 'total_cycle_exposure' missing in audit report."

    expected_cycles = 2
    expected_exposure = 630

    actual_cycles = data["total_3_cycles"]
    actual_exposure = data["total_cycle_exposure"]

    assert actual_cycles == expected_cycles, f"Expected total_3_cycles to be {expected_cycles}, got {actual_cycles}."
    assert actual_exposure == expected_exposure, f"Expected total_cycle_exposure to be {expected_exposure}, got {actual_exposure}."