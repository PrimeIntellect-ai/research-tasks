# test_final_state.py
import os

def test_c_file_exists():
    c_file_path = "/home/user/clean_and_search.c"
    assert os.path.isfile(c_file_path), f"The C source file is missing at {c_file_path}. You must write your program to this location."

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"The output file is missing at {result_path}. Did you run your program and save the output?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = "38, 45, 68, 86"
    assert expected in content, f"The result file {result_path} contains incorrect output. Expected it to contain '{expected}', but found '{content}'."