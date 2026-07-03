# test_final_state.py
import os

def test_debug_result_content():
    path = "/home/user/debug_result.txt"
    assert os.path.isfile(path), f"Verification failed: {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "ID: 3412, CORRECT_HASH: 15"
    assert content == expected, f"Verification failed. Expected '{expected}', got '{content}'."

def test_cpp_file_exists():
    path = "/home/user/process_queries.cpp"
    assert os.path.isfile(path), f"Verification failed: {path} does not exist."