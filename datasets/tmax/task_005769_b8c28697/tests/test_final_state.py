# test_final_state.py

import os

def test_result_file_exists():
    path = "/home/user/tester/result.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. Did you run the executable?"

def test_result_file_content():
    path = "/home/user/tester/result.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "168", f"Expected result.txt to contain '168', but found '{content}'."