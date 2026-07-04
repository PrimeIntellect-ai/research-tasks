# test_final_state.py

import os
import pytest

def test_analyzer_c_exists():
    path = "/home/user/analyzer.c"
    assert os.path.exists(path), f"Source file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_analyzer_executable_exists():
    path = "/home/user/analyzer"
    assert os.path.exists(path), f"Executable file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_leaf_chains_csv():
    path = "/home/user/leaf_chains.csv"
    assert os.path.exists(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip().replace("\r", "")

    expected = "7,5280\n6,5270\n5,5225\n10,2150"
    assert content == expected, f"Content of {path} does not match expected output.\nExpected:\n{expected}\nActual:\n{content}"

def test_top_ancestor_txt():
    path = "/home/user/top_ancestor.txt"
    assert os.path.exists(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "1"
    assert content == expected, f"Content of {path} does not match expected output.\nExpected: '{expected}', Actual: '{content}'"