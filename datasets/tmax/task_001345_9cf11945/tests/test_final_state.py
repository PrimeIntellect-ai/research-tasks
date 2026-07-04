# test_final_state.py

import os
import pytest

def test_infer_c_exists():
    path = "/home/user/infer.c"
    assert os.path.isfile(path), f"File {path} is missing. You need to write the C program."

def test_infer_executable_exists():
    path = "/home/user/infer"
    assert os.path.isfile(path), f"Executable {path} is missing. You need to compile your C program."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_scores_csv_correct():
    path = "/home/user/scores.csv"
    assert os.path.isfile(path), f"File {path} is missing. You need to run the pipeline and save results."

    expected_content = """id,score
1,12.0
2,26.0
3,25.0
4,8.8
5,0.0"""

    with open(path, "r") as f:
        content = f.read().strip()

    # Normalize line endings
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, f"Content of {path} does not match the expected output. Got:\n{content}"