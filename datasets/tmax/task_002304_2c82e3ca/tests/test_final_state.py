# test_final_state.py

import os
import pytest

def test_extract_c_exists():
    path = '/home/user/extract.c'
    assert os.path.exists(path), f"The file {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."

def test_extract_executable_exists():
    path = '/home/user/extract'
    assert os.path.exists(path), f"The executable {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_top_sessions_output():
    path = '/home/user/top_sessions.txt'
    assert os.path.exists(path), f"The file {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip().splitlines()

    # Clean up any trailing/leading whitespace per line
    content = [line.strip() for line in content if line.strip()]

    expected = ['aaaaaaaa', 'bbbbbbbb', 'cccccccc']

    assert len(content) == 3, f"Expected exactly 3 lines in {path}, but got {len(content)}."
    assert content == expected, f"Expected {expected} in {path}, but got {content}."