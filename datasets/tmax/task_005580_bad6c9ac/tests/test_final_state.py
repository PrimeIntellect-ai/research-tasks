# test_final_state.py

import os
import pytest

def test_resolver_c_exists():
    path = "/home/user/build_env/resolver.c"
    assert os.path.isfile(path), f"The file {path} does not exist. You must create the C implementation."

def test_validator_executable_exists():
    path = "/home/user/build_env/validator"
    assert os.path.isfile(path), f"The executable {path} does not exist. Make sure you ran 'make'."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_output_log_exists_and_content():
    path = "/home/user/build_env/output.log"
    assert os.path.isfile(path), f"The file {path} does not exist. Make sure you ran the executable and redirected output."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Resolved Dependencies: 5"
    assert expected in content, f"The output.log does not contain the expected result. Expected '{expected}', got '{content}'."