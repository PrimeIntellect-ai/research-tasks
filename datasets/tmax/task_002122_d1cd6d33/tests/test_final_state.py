# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_incident_report_contents():
    """Verify the incident report contains the correct poison pill value and success message."""
    report_path = "/home/user/incident_report.txt"
    assert os.path.exists(report_path), f"Incident report is missing at {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip() != ""]

    assert len(lines) == 2, f"Expected exactly 2 lines in incident report, found {len(lines)}."
    assert lines[0] == "0", f"Expected the first line to be the poison pill value '0', but got '{lines[0]}'."
    assert lines[1] == "SUCCESS", f"Expected the second line to be 'SUCCESS', but got '{lines[1]}'."

def test_validate_script_passes():
    """Run the validation script and ensure it exits with code 0 without hanging."""
    validate_path = "/home/user/validate.py"
    assert os.path.exists(validate_path), f"Validation script missing at {validate_path}"

    try:
        # Run the script with a timeout to catch infinite loops
        result = subprocess.run(
            [sys.executable, validate_path],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("validate.py timed out. The infinite loop for n <= 0 in math_service.py has not been fixed.")

    assert result.returncode == 0, (
        f"validate.py failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_math_service_logic_directly():
    """Directly import and test the math_service to ensure n <= 0 returns an empty list."""
    sys.path.insert(0, "/home/user")
    try:
        import math_service
    except ImportError:
        pytest.fail("Failed to import math_service.py from /home/user.")

    # We use multiprocessing to safely test the function with a timeout, 
    # but since validate.py already covers the timeout, we can just rely on the subprocess test above.
    # However, we can do a quick check for another negative number to be thorough.
    # We'll trust the validate script's timeout to have proven the loop is broken.
    try:
        result = math_service.compute_collatz(-99)
        assert result == [], f"Expected compute_collatz(-99) to return [], but got {result}"
    except Exception as e:
        pytest.fail(f"compute_collatz raised an exception for n <= 0: {e}")