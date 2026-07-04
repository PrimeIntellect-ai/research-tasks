# test_final_state.py

import os
import pytest

def test_projected_edges():
    file_path = "/home/user/projected_edges.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_content = """C,D,15
C,E,10
D,END,5
E,F,5
START,A,10
START,C,5
START,E,20"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} does not match the expected projected edges."

def test_shortest_path():
    file_path = "/home/user/shortest_path.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_content = """0,START
1,C
2,D
3,END"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} does not match the expected shortest path."

def test_find_path_script():
    file_path = "/home/user/find_path.sh"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."