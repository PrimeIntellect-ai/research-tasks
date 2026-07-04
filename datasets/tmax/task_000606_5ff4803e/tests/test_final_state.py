# test_final_state.py

import os
import json
import glob
import pytest

def compute_expected_violations():
    """Computes the expected violations dynamically from the log files."""
    expected = {}
    log_files = glob.glob("/home/user/sim_logs/node_*.log")

    for filepath in log_files:
        filename = os.path.basename(filepath)
        node_name = filename.replace(".log", "")

        violations = 0
        prev_error = 0.0
        prev_step = 0.0

        with open(filepath, "r") as f:
            for i, line in enumerate(f):
                parts = line.strip().split()
                if len(parts) != 3:
                    continue

                step = float(parts[1])
                error = float(parts[2])

                if i > 0 and prev_error > 0.005:
                    # Using a small epsilon to handle floating point inaccuracies
                    if step > (prev_step * 0.5) + 1e-7:
                        violations += 1

                prev_error = error
                prev_step = step

        if violations > 0:
            expected[node_name] = violations

    return expected

def test_audit_script_exists_and_executable():
    """Test that the audit script exists and is executable."""
    script_path = "/home/user/audit_sim.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_json_exists():
    """Test that the report.json file exists."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

def test_report_json_content():
    """Test that the report.json contains the correct violation counts."""
    report_path = "/home/user/report.json"

    try:
        with open(report_path, "r") as f:
            actual_report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_report = compute_expected_violations()

    assert isinstance(actual_report, dict), "The JSON report should be a dictionary."
    assert actual_report == expected_report, f"Report content mismatch. Expected: {expected_report}, but got: {actual_report}"