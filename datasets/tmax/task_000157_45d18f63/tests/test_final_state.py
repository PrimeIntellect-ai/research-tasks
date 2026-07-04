# test_final_state.py

import os
import re
import subprocess
import pytest

def test_simulate_cpp_updated():
    path = "/home/user/simulate.cpp"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # Extract main function to check initial distance
    main_match = re.search(r'int\s+main\s*\(\s*\)\s*\{([^}]+)\}', content, re.MULTILINE)
    assert main_match is not None, "Could not find main function in simulate.cpp."
    main_body = main_match.group(1)

    # Check for x = 5.0 or x = 5
    assert re.search(r'double\s+x\s*=\s*5(\.0*)?\s*;', main_body), "Initial distance in simulate.cpp was not updated to 5.0."

    # Verify that the step size adjustment logic has been modified
    # We expect 0.5 and 1.5 to be present in the file for the fixed logic
    assert "0.5" in content and "1.5" in content, "simulate.cpp does not contain the expected step size adjustment factors (0.5 and 1.5)."

def test_result_txt():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"result.txt does not contain a valid float: '{content}'")

    assert 2.217 <= val <= 2.227, f"result.txt value {val} is not within the expected range [2.217, 2.227]."

def test_validate_sh():
    path = "/home/user/validate.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Run the script and check exit code
    try:
        result = subprocess.run([path], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("validate.sh timed out after 10 seconds.")

    assert result.returncode == 0, f"validate.sh exited with code {result.returncode}, expected 0. Stderr: {result.stderr}"