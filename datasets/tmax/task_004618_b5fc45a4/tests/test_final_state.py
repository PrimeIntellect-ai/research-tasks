# test_final_state.py

import os
import subprocess
import pytest
import re

APP_DIR = "/home/user/app"
REQ_FILE = os.path.join(APP_DIR, "requirements.txt")
STATS_FILE = os.path.join(APP_DIR, "stats_calculator.py")
STRESS_TEST_FILE = os.path.join(APP_DIR, "stress_test.sh")

def test_requirements_fixed():
    """Verify requirements.txt is fixed and installable."""
    assert os.path.isfile(REQ_FILE), f"{REQ_FILE} does not exist."
    with open(REQ_FILE, "r") as f:
        content = f.read()

    # Check that scipy is not downgraded (should be 1.10.1 or at least present without a lower version)
    assert "scipy" in content.lower(), "scipy is missing from requirements.txt"

    # Run pip install dry-run to ensure resolution works
    result = subprocess.run(
        ["pip", "install", "--dry-run", "-r", REQ_FILE],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pip install failed to resolve dependencies:\n{result.stderr}"

def test_stress_test_exists_and_executable():
    """Verify stress_test.sh exists and is executable."""
    assert os.path.isfile(STRESS_TEST_FILE), f"{STRESS_TEST_FILE} does not exist."
    assert os.access(STRESS_TEST_FILE, os.X_OK), f"{STRESS_TEST_FILE} is not executable."

def test_python_script_fixed():
    """Verify stats_calculator.py uses threading or similar locking mechanism."""
    assert os.path.isfile(STATS_FILE), f"{STATS_FILE} does not exist."
    with open(STATS_FILE, "r") as f:
        content = f.read()

    # Look for threading import and lock usage
    has_threading = "threading" in content or "Lock" in content or "multiprocessing" in content
    assert has_threading, "No locking mechanism (e.g., threading.Lock) found in stats_calculator.py."

def test_stress_test_execution():
    """Verify that running the stress test completes successfully (exit code 0)."""
    # Run the stress test script
    result = subprocess.run(
        [STRESS_TEST_FILE],
        cwd=APP_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"stress_test.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "Race condition reproduced" not in result.stdout, "Stress test output indicates the race condition is still present."