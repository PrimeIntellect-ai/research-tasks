# test_final_state.py
import os
import pytest

def test_parser_cpp_exists():
    cpp_file = '/home/user/parser.cpp'
    assert os.path.exists(cpp_file), f"Source file {cpp_file} does not exist. You must write your code in this file."
    assert os.path.isfile(cpp_file), f"Path {cpp_file} is not a file."

def test_valid_deployments_output():
    output_file = '/home/user/valid_deployments.txt'
    assert os.path.exists(output_file), f"Output file {output_file} does not exist. Ensure your C++ program writes to this file."
    assert os.path.isfile(output_file), f"Path {output_file} is not a regular file."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    expected_content = "1,2,4"
    assert content == expected_content, f"The contents of {output_file} are incorrect. Expected '{expected_content}', but got '{content}'."