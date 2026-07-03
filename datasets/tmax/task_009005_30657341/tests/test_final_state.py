# test_final_state.py

import os
import subprocess
import sys

PROJECT_DIR = "/home/user/project"
API_PY = os.path.join(PROJECT_DIR, "api.py")
MATH_OPS_PY = os.path.join(PROJECT_DIR, "math_ops.py")
UTILS_PY = os.path.join(PROJECT_DIR, "utils.py")
TEST_API_PY = os.path.join(PROJECT_DIR, "test_api.py")
RESOLUTION_TXT = "/home/user/resolution.txt"

def test_pytest_passes():
    """Verify that the test suite passes successfully, meaning no circular imports and logic is correct."""
    assert os.path.isfile(TEST_API_PY), f"Test file {TEST_API_PY} is missing."

    # Run pytest on the test_api.py file
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_API_PY],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed. Output:\n{result.stdout}\n{result.stderr}"

def test_utils_py_exists_and_has_logger():
    """Verify that utils.py was created and contains the logger function."""
    assert os.path.isfile(UTILS_PY), f"File {UTILS_PY} does not exist. Did you extract the logger component?"

    with open(UTILS_PY, "r") as f:
        content = f.read()

    assert "def logger" in content, f"{UTILS_PY} does not contain the 'logger' function definition."

def test_logger_removed_from_api_py():
    """Verify that logger is no longer defined in api.py."""
    assert os.path.isfile(API_PY), f"File {API_PY} does not exist."

    with open(API_PY, "r") as f:
        content = f.read()

    assert "def logger" not in content, f"{API_PY} still contains the 'logger' function definition. It should be moved to utils.py."

def test_resolution_txt():
    """Verify that resolution.txt exists and contains the correct modified files."""
    assert os.path.isfile(RESOLUTION_TXT), f"File {RESOLUTION_TXT} does not exist."

    with open(RESOLUTION_TXT, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_files = {"api.py", "math_ops.py", "utils.py"}
    actual_files = set(lines)

    missing = expected_files - actual_files
    assert not missing, f"{RESOLUTION_TXT} is missing the following required files: {missing}"