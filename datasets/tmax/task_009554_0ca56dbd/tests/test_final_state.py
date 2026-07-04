# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import pytest

SCRIPT_DIR = "/home/user/ticket_4092"
PYTHON_SCRIPT = os.path.join(SCRIPT_DIR, "process_jobs.py")
REGRESSION_SCRIPT = os.path.join(SCRIPT_DIR, "regression_test.sh")

def test_regression_script_exists_and_executable():
    """Test that regression_test.sh exists and is executable."""
    assert os.path.isfile(REGRESSION_SCRIPT), f"{REGRESSION_SCRIPT} does not exist."
    assert os.access(REGRESSION_SCRIPT, os.X_OK), f"{REGRESSION_SCRIPT} is not executable."

def test_process_jobs_fixed():
    """Test that process_jobs.py reliably outputs 1000000."""
    assert os.path.isfile(PYTHON_SCRIPT), f"{PYTHON_SCRIPT} does not exist."

    for i in range(5):
        result = subprocess.run(
            ["python3", PYTHON_SCRIPT],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"process_jobs.py failed with return code {result.returncode}"
        output = result.stdout.strip()
        assert output == "1000000", f"Run {i+1}: process_jobs.py output '{output}', expected '1000000'. Race condition might not be fully fixed."

def test_regression_script_success_behavior():
    """Test that regression_test.sh exits 0 when process_jobs.py is correct."""
    # Since process_jobs.py is already verified to be correct by test_process_jobs_fixed,
    # regression_test.sh should exit 0.
    result = subprocess.run([REGRESSION_SCRIPT], capture_output=True)
    assert result.returncode == 0, f"regression_test.sh should exit 0 for a correct process_jobs.py, but exited {result.returncode}."

def test_regression_script_failure_behavior():
    """Test that regression_test.sh exits 1 when process_jobs.py is incorrect."""
    # Backup the original process_jobs.py
    backup_path = PYTHON_SCRIPT + ".bak"
    shutil.copy2(PYTHON_SCRIPT, backup_path)

    try:
        # Inject a failing script
        with open(PYTHON_SCRIPT, "w") as f:
            f.write("print(999999)\n")

        result = subprocess.run([REGRESSION_SCRIPT], capture_output=True)
        assert result.returncode == 1, f"regression_test.sh should exit 1 when process_jobs.py outputs wrong values, but exited {result.returncode}."
    finally:
        # Restore the original script
        shutil.move(backup_path, PYTHON_SCRIPT)