# test_final_state.py

import os
import pytest

def test_inference_rs_exists():
    file_path = "/home/user/inference.rs"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you write the Rust program?"

def test_best_category_txt_exists_and_content():
    file_path = "/home/user/best_category.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run your Rust program to generate the output?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "gamma,5.0000"
    assert expected in content, f"Expected '{expected}' in {file_path}, but got '{content}'"

def test_rust_executable_exists():
    # rustc /home/user/inference.rs -O produces /home/user/inference or inference in the current dir
    # we just check if the output file is generated in /home/user/
    executable_path = "/home/user/inference"
    assert os.path.isfile(executable_path) and os.access(executable_path, os.X_OK), \
        f"Executable {executable_path} not found or not executable. Did you compile with rustc?"