# test_final_state.py
import os
import json
import subprocess
import pytest

REPORT_PATH = "/home/user/fix_report.json"
BINARY_PATH = "/home/user/engine/process"
INPUT_PATH = "/home/user/engine/input.txt"

def test_report_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("fix_report.json is not valid JSON")

    assert "crashing_line_index" in report, "Missing 'crashing_line_index' in report"
    assert "fixed_binary_path" in report, "Missing 'fixed_binary_path' in report"

    assert report["crashing_line_index"] == 421, f"Expected crashing_line_index 421, got {report['crashing_line_index']}"
    assert report["fixed_binary_path"] == BINARY_PATH, f"Expected fixed_binary_path {BINARY_PATH}, got {report['fixed_binary_path']}"

def test_binary_runs_successfully():
    assert os.path.isfile(BINARY_PATH), f"Binary {BINARY_PATH} does not exist."
    assert os.access(BINARY_PATH, os.X_OK), f"Binary {BINARY_PATH} is not executable."

    res = subprocess.run([BINARY_PATH, INPUT_PATH], capture_output=True)
    assert res.returncode == 0, f"Binary failed with return code {res.returncode}. Stderr: {res.stderr.decode()}"

    # Optionally, verify that the binary processed the 1000 lines
    stdout = res.stdout.decode()
    assert "1000" in stdout, f"Binary did not seem to process all 1000 lines. Stdout: {stdout}"