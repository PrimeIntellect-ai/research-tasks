# test_final_state.py

import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/engine"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} does not exist. Did you compile the code?"
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_view_txt_exists_and_correct():
    view_path = "/home/user/view.txt"
    assert os.path.isfile(view_path), f"The output file {view_path} does not exist. Did the program run successfully without deadlocking?"

    with open(view_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "0,9,200",
        "3,4,120",
        "5,6,120"
    ]

    assert lines == expected, (
        f"The contents of {view_path} are incorrect.\n"
        f"Expected:\n{expected}\n"
        f"Got:\n{lines}\n"
        "Ensure filtering (amount >= 50), sorting (amount desc, src asc, dst asc), and pagination (limit 3, offset 0) are correctly implemented."
    )