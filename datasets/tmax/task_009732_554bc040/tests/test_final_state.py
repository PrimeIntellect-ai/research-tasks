# test_final_state.py

import os
import subprocess
import pytest

def test_test_file_exists():
    """Verify that the test file was created."""
    assert os.path.isfile("/home/user/test_math_utility.py"), "The file /home/user/test_math_utility.py is missing."

def test_results_file_exists():
    """Verify that the test results file was created."""
    assert os.path.isfile("/home/user/test_results.txt"), "The file /home/user/test_results.txt is missing."

def test_test_file_contents():
    """Verify that the test file contains the required test cases and uses mock."""
    with open("/home/user/test_math_utility.py", "r", encoding="utf-8") as f:
        content = f.read()

    assert "def test_legacy_version_fallback" in content, "Missing test_legacy_version_fallback in test_math_utility.py."
    assert "def test_modern_version_abi" in content, "Missing test_modern_version_abi in test_math_utility.py."
    assert "mock" in content, "Missing mock usage in test_math_utility.py."

def test_pytest_passes():
    """Verify that the tests written in test_math_utility.py pass successfully."""
    # We run pytest on the user's test file.
    result = subprocess.run(
        ["python3", "-m", "pytest", "/home/user/test_math_utility.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed on test_math_utility.py.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"