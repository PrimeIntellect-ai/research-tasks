# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/ticket_8831"
PROCESSOR_CPP = os.path.join(BASE_DIR, "processor.cpp")
DATA_TXT = os.path.join(BASE_DIR, "data.txt")
TEST_SH = os.path.join(BASE_DIR, "test.sh")
RESOLUTION_LOG = os.path.join(BASE_DIR, "resolution.log")

def test_processor_cpp_fixed():
    """Test that processor.cpp has been fixed according to requirements."""
    assert os.path.isfile(PROCESSOR_CPP), f"File {PROCESSOR_CPP} does not exist."

    with open(PROCESSOR_CPP, 'r') as f:
        content = f.read()

    # Check for precision changes
    assert "std::vector<double>" in content or "vector<double>" in content, "Did not find vector<double> in processor.cpp"
    assert "float" not in content, "Found 'float' in processor.cpp, it should be completely replaced with 'double'"

    # Check for boundary condition fixes (loop starting at 0 and ending at < n)
    assert "i = 1" not in content, "Loop still appears to start at 1 (off-by-one error)."
    assert "<= n" not in content, "Loop still appears to go up to <= n (off-by-one error)."

    # Check for at least two assert statements
    assert content.count("assert(") >= 2, "processor.cpp must contain at least two assert() statements."

def test_test_sh_exists_and_executable():
    """Test that test.sh exists and is executable."""
    assert os.path.isfile(TEST_SH), f"File {TEST_SH} does not exist."
    assert os.access(TEST_SH, os.X_OK), f"File {TEST_SH} is not executable."

def test_test_sh_execution():
    """Test that executing test.sh compiles and runs successfully."""
    result = subprocess.run([TEST_SH], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"test.sh failed to execute with exit code 0. Stderr: {result.stderr}"

def test_resolution_log():
    """Test that resolution.log contains the correct computed total."""
    assert os.path.isfile(RESOLUTION_LOG), f"File {RESOLUTION_LOG} does not exist."

    with open(RESOLUTION_LOG, 'r') as f:
        content = f.read().strip()

    # The expected exact sum of 100,000 entries of 1000.01
    expected_sum = "100001000.000000"

    # We check if the expected sum is in the log (allowing for potential newlines or extra text)
    assert expected_sum in content, f"resolution.log does not contain the correct sum '{expected_sum}'. Content found: '{content}'"