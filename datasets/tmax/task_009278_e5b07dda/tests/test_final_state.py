# test_final_state.py

import os
import pytest

def test_cycles_txt_exists_and_content():
    cycles_path = "/home/user/cycles.txt"
    assert os.path.isfile(cycles_path), f"File {cycles_path} does not exist. Did you compile and run your C++ program?"

    with open(cycles_path, "r") as f:
        # Read lines, strip whitespace, and ignore empty lines
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "101,102,103",
        "101,103,104"
    ]

    assert lines == expected_lines, (
        f"Content of {cycles_path} is incorrect.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{lines}"
    )