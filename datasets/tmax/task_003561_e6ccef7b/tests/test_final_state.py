# test_final_state.py
import os

def test_result_file_exists():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you write the output to the correct location?"

def test_result_file_contents():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_content = "Beta, 18.23"
    assert content == expected_content, f"Contents of {path} are incorrect. Expected '{expected_content}', but got '{content}'."