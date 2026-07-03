# test_final_state.py

import os
import pytest

def test_recovered_dat_exists():
    path = "/home/user/recovered.dat"
    assert os.path.isfile(path), f"Expected file {path} does not exist. You need to recover crash.dat."
    assert os.path.getsize(path) > 0, f"Recovered file {path} is empty."

def test_mre_c_exists():
    path = "/home/user/mre.c"
    assert os.path.isfile(path), f"Expected file {path} does not exist. You need to write the MRE."
    assert os.path.getsize(path) > 0, f"File {path} is empty."

def test_error_log_contents():
    path = "/home/user/error.log"
    assert os.path.isfile(path), f"Expected file {path} does not exist. You need to run your MRE and redirect output."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Error: 331"
    assert content == expected, f"File {path} content is incorrect. Expected '{expected}', got '{content}'."