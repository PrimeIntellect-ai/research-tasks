# test_final_state.py

import os
import json
import subprocess
import pytest

def test_go_program_fixed():
    """Verify that the Go program runs successfully without hanging (deadlock fixed)."""
    go_file = "/home/user/processor.go"
    assert os.path.isfile(go_file), f"{go_file} does not exist."

    try:
        # Run the go program with a timeout to detect deadlocks
        result = subprocess.run(
            ["go", "run", go_file],
            capture_output=True,
            timeout=5
        )
        assert result.returncode == 0, f"Go program failed with exit code {result.returncode}.\nStderr: {result.stderr.decode('utf-8', errors='replace')}"
    except subprocess.TimeoutExpired:
        pytest.fail("Go program timed out after 5 seconds. The deadlock is likely not fixed.")

def test_e2e_script_exists_and_runs():
    """Verify that the Python E2E script exists and runs successfully."""
    script_path = "/home/user/e2e_test.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    report_path = "/home/user/test_report.json"
    # Remove the report file if it exists to ensure the script actually creates it
    if os.path.exists(report_path):
        os.remove(report_path)

    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            timeout=10
        )
        assert result.returncode == 0, f"e2e_test.py failed with exit code {result.returncode}.\nStderr: {result.stderr.decode('utf-8', errors='replace')}"
    except subprocess.TimeoutExpired:
        pytest.fail("e2e_test.py timed out after 10 seconds.")

    assert os.path.isfile(report_path), f"e2e_test.py did not create {report_path}."

def test_report_json_content():
    """Verify that test_report.json contains the correct counts."""
    report_path = "/home/user/test_report.json"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not a valid JSON file.")

    assert "utf8_count" in data, "Key 'utf8_count' missing from test_report.json"
    assert "shiftjis_count" in data, "Key 'shiftjis_count' missing from test_report.json"

    assert data["utf8_count"] == 10, f"Expected utf8_count to be 10, got {data['utf8_count']}"
    assert data["shiftjis_count"] == 15, f"Expected shiftjis_count to be 15, got {data['shiftjis_count']}"