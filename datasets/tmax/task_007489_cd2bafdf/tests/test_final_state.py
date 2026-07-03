# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/anonymize.sh"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    test_input = """  User ALICE reached out at Alice.Smith+123@domain.com for support.  
Call me at 555-123-4567 regarding the server issue.
  user alice reached out at alice.smith+123@domain.com for support.
Contact billing at (800) 555-9999 or admin@corp.net immediately!


We need more RAM.
we need more ram.  
"""

    expected_output = """call me at [phone] regarding the server issue.
contact billing at [phone] or [email] immediately!
user alice reached out at [email] for support.
we need more ram.
"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as infile:
        infile.write(test_input)
        in_path = infile.name

    out_path = in_path + "_out"

    try:
        result = subprocess.run(
            [SCRIPT_PATH, in_path, out_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

        assert os.path.exists(out_path), "Script did not create the output file."

        with open(out_path, "r") as f:
            actual_output = f.read()

        assert actual_output == expected_output, (
            f"Output file content does not match expected.\n"
            f"Expected:\n{expected_output}\n"
            f"Actual:\n{actual_output}"
        )
    finally:
        if os.path.exists(in_path):
            os.remove(in_path)
        if os.path.exists(out_path):
            os.remove(out_path)