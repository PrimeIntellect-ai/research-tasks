# test_final_state.py
import os

def test_solution_file_exists():
    path = "/home/user/solution.txt"
    assert os.path.isfile(path), f"Expected solution file {path} does not exist."

def test_solution_content():
    path = "/home/user/solution.txt"
    with open(path, 'r') as f:
        content = f.read().strip()
    expected = "2023-11-05 01:15"
    assert content == expected, f"Solution file content is incorrect. Expected '{expected}', got '{content}'."