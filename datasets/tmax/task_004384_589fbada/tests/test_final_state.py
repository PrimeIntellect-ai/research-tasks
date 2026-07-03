# test_final_state.py
import os

def test_result_file_exists():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"The file {result_path} does not exist. Did you save the result?"

def test_result_content():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"The file {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected = "8456.1230"
    assert content == expected, f"The content of {result_path} is incorrect. Expected '{expected}', but got '{content}'."