# test_final_state.py

import os

def test_c_source_exists():
    path = "/home/user/boot_corr.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_executable_exists():
    path = "/home/user/boot_corr"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_result_txt_content():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert "0.9984" in content, f"Expected '0.9984' in {path}, but found '{content}'."