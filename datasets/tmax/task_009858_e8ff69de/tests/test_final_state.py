# test_final_state.py

import os
import py_compile
import pytest

def test_modern_parser_exists_and_valid():
    file_path = "/home/user/modern_parser.py"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    try:
        py_compile.compile(file_path, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"{file_path} is not a valid Python 3 script. Compilation failed: {e}")

def test_output_txt_content():
    file_path = "/home/user/output.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you save the output?"

    expected_content = """result {
  context_id: "alpha"
  value: 40
}
result {
  context_id: "beta"
  value: 58
}
result {
  context_id: "gamma"
  value: 7
}"""

    with open(file_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {file_path} does not match the expected protobuf-like text format."