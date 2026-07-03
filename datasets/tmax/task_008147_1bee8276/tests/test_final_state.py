# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    source_path = "/home/user/find_restore_path.c"
    assert os.path.isfile(source_path), f"C source file {source_path} is missing."

def test_executable_exists_and_is_executable():
    executable_path = "/home/user/find_restore_path"
    assert os.path.isfile(executable_path), f"Executable file {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_output_file_content():
    output_path = "/home/user/path_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_output = "RESTORE_PATH: 42 -> 8 -> 3 -> 1"
    assert expected_output in content, f"Output file content is incorrect. Expected to find '{expected_output}', but got:\n{content}"