# test_final_state.py

import os
import json
import subprocess
import pytest

def test_executable_exists_and_compiled():
    """Verify that the fast-det executable has been compiled and exists."""
    exe_path = "/home/user/fast-det/fast-det"
    assert os.path.exists(exe_path), "The executable /home/user/fast-det/fast-det does not exist. Did the Makefile build it?"
    assert os.path.isfile(exe_path), f"Expected {exe_path} to be a file."
    assert os.access(exe_path, os.X_OK), f"Expected {exe_path} to be executable."

def test_fast_det_runs():
    """Verify that the compiled fast-det works correctly on a simple matrix."""
    exe_path = "/home/user/fast-det/fast-det"
    # Identity matrix 2x2
    result = subprocess.run([exe_path, "2", "1", "0", "0", "1"], capture_output=True, text=True)
    assert result.returncode == 0, f"fast-det failed to run. Stderr: {result.stderr}"
    assert result.stdout.strip() == "1", f"Expected determinant of 2x2 identity matrix to be 1, got '{result.stdout.strip()}'"

def test_pr_summary_json():
    """Verify that the test runner generated the correct JSON report."""
    json_path = "/home/user/pr_summary.json"
    assert os.path.exists(json_path), f"The report file {json_path} does not exist. Did you run the test_runner.sh script?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert "passed" in data, "JSON report is missing the 'passed' key."
    assert "failed" in data, "JSON report is missing the 'failed' key."
    assert "total" in data, "JSON report is missing the 'total' key."

    assert data["passed"] == 3, f"Expected 3 passed tests, got {data['passed']}."
    assert data["failed"] == 0, f"Expected 0 failed tests, got {data['failed']}."
    assert data["total"] == 3, f"Expected 3 total tests, got {data['total']}."

def test_c_code_fixed():
    """Verify that the C code includes math.h."""
    c_path = "/home/user/fast-det/src/determinant.c"
    with open(c_path, "r") as f:
        content = f.read()
    assert "<math.h>" in content, "The file determinant.c does not seem to include <math.h>."

def test_makefile_fixed():
    """Verify that the Makefile links the math library."""
    makefile_path = "/home/user/fast-det/Makefile"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, "The Makefile does not seem to link the math library (-lm)."