# test_final_state.py

import os
import pytest

def test_math_success_log_exists():
    log_path = "/home/user/math_success.log"
    assert os.path.isfile(log_path), f"Expected output file {log_path} does not exist. Did the Python script run successfully?"

def test_math_success_log_content():
    log_path = "/home/user/math_success.log"
    assert os.path.isfile(log_path), f"Expected output file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    expected_content = "RESULT: 120\n"
    assert content == expected_content, f"Content of {log_path} is incorrect. Expected {repr(expected_content)}, but got {repr(content)}"

def test_rust_server_compiled():
    binary_path = "/home/user/math_feature/server"
    assert os.path.isfile(binary_path), f"Expected compiled Rust binary {binary_path} does not exist. Did you compile server.rs?"
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} exists but is not executable."