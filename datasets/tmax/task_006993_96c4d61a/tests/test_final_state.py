# test_final_state.py

import os
import pytest

def test_makefile_patched():
    makefile_path = "/home/user/hybrid_project/c_lib/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-shared -fPIC" in content, "Makefile was not correctly patched with -shared and -fPIC flags."

def test_shared_library_compiled():
    so_path = "/home/user/hybrid_project/c_lib/libtransform.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled."
    assert os.access(so_path, os.R_OK), f"Shared library {so_path} is not readable."

def test_ws_response_file_content():
    response_file = "/home/user/ws_response.txt"
    assert os.path.isfile(response_file), f"Response file {response_file} does not exist."

    # Compute the expected response based on the task description
    input_str = "OrganizeFiles"
    expected_response = input_str[::-1] + "_processed"

    with open(response_file, "r") as f:
        actual_response = f.read().strip()

    assert actual_response == expected_response, f"Expected '{expected_response}' but got '{actual_response}' in {response_file}."