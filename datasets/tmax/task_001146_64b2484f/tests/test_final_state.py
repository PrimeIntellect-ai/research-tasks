# test_final_state.py

import os
import pytest

def test_summary_txt_exists_and_content():
    file_path = "/home/user/summary.txt"

    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did you run the program?"

    expected_content = (
        "Group A: Mean=3.25, CI=[1.78, 4.72]\n"
        "Group B: Mean=2.75, CI=[1.08, 4.42]"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {file_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )