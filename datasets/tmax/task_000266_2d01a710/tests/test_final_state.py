# test_final_state.py
import os

def test_c_source_exists():
    path = "/home/user/process_graph.c"
    assert os.path.isfile(path), f"C source file {path} does not exist. You must write your solution in this file."

def test_page2_results_exists():
    path = "/home/user/page2_results.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did your program run and produce it?"

def test_page2_results_content():
    path = "/home/user/page2_results.txt"
    expected_lines = [
        "7 3",
        "8 3",
        "9 3"
    ]

    with open(path, "r") as f:
        # Read lines, strip whitespace from ends, and ignore empty lines
        content = [line.strip() for line in f.readlines() if line.strip()]

    assert content == expected_lines, f"Content of {path} is incorrect.\nExpected:\n{expected_lines}\nGot:\n{content}"