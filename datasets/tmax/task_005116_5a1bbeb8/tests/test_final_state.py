# test_final_state.py

import os
import pytest

def test_libmock_so_exists():
    path = "/home/user/project/libmock.so"
    assert os.path.isfile(path), f"Mock shared library {path} is missing."

def test_leak_size_file_exists():
    path = "/home/user/project/leak_size.txt"
    assert os.path.isfile(path), f"Result file {path} is missing."

def test_leak_size_correct():
    path = "/home/user/project/leak_size.txt"
    assert os.path.isfile(path), f"Result file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "256", f"Expected leak size to be '256', but got '{content}'."