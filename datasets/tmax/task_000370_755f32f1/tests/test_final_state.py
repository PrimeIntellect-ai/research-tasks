# test_final_state.py

import os
import subprocess
import pytest

def test_buggy_line_num():
    path = "/home/user/buggy_line_num.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "3456", f"Expected buggy line number to be '3456', but got '{content}'."

def test_mre_py():
    path = "/home/user/mre.py"
    assert os.path.isfile(path), f"Expected MRE script {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check that it doesn't open files
    assert "open(" not in content, "MRE script should not read external files (found 'open(')."

    # Check that it hardcodes the data
    assert "100000001.0" in content and "100000005.0" in content, "MRE script does not seem to hardcode the buggy data."
    assert "data" in content, "MRE script must define a variable named 'data'."

    # Run the script and check for ValueError
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    assert result.returncode != 0, "MRE script should crash, but it exited successfully."
    assert "ValueError" in result.stderr, "MRE script should raise a ValueError."

def test_stable_result():
    path = "/home/user/stable_result.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "1.4142", f"Expected stable result to be '1.4142', but got '{content}'."