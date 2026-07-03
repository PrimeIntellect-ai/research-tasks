# test_final_state.py
import os

def test_shortest_path_file():
    path = '/home/user/shortest_path.txt'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected = "Apex_Holdings,Bravo_Corp,Delta_LLC,Zeta_Retail"
    assert content == expected, f"Expected shortest path '{expected}', but got '{content}'"

def test_page2_file():
    path = '/home/user/page2.txt'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["Delta_LLC", "Echo_Group"]
    assert lines == expected, f"Expected page 2 entities {expected}, but got {lines}"