# test_final_state.py

import os
import subprocess
import pytest

BAD_COMMIT_MSG_PATH = "/home/user/bad_commit_message.txt"
FIXED_AREA_PATH = "/home/user/fixed_area.txt"
REPO_PATH = "/home/user/math_repo"
SCRIPT_PATH = os.path.join(REPO_PATH, "calc_integral.sh")

def test_bad_commit_message():
    assert os.path.isfile(BAD_COMMIT_MSG_PATH), f"File {BAD_COMMIT_MSG_PATH} does not exist"
    with open(BAD_COMMIT_MSG_PATH, "r") as f:
        content = f.read().strip()
    expected_msg = "Refactor integration loop 137"
    assert content == expected_msg, f"Expected bad commit message to be '{expected_msg}', but got '{content}'"

def test_fixed_area_output():
    assert os.path.isfile(FIXED_AREA_PATH), f"File {FIXED_AREA_PATH} does not exist"
    with open(FIXED_AREA_PATH, "r") as f:
        content = f.read().strip()
    expected_area = "1000.0000"
    assert content == expected_area, f"Expected fixed area to be '{expected_area}', but got '{content}'"

def test_script_is_fixed():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist"
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "sum+=((y1+y2)/2)*dx" in content.replace(" ", ""), "The formula in calc_integral.sh is still incorrect or not using the trapezoidal rule properly (missing division by 2)."

def test_script_execution():
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"
    result = subprocess.run(
        [SCRIPT_PATH],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}"
    output = result.stdout.strip()
    assert output == "1000.0000", f"Expected script to output '1000.0000', but got '{output}'"