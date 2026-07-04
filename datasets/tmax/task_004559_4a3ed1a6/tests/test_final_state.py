# test_final_state.py

import os
import pytest

def test_secure_output_exists_and_correct():
    """Check that secure_output.txt exists and contains the expected results."""
    file_path = "/home/user/calculator/secure_output.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_lines = ["12", "76", "50", "-1"]

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Content of {file_path} does not match expected values. Got {lines}, expected {expected_lines}."

def test_rust_shared_object_exists():
    """Check that the compiled Rust shared object exists."""
    so_path = "/home/user/calculator/safe_eval/target/release/libsafe_eval.so"
    assert os.path.exists(so_path), f"Shared object {so_path} does not exist. Did you build the Rust library in release mode?"
    assert os.path.isfile(so_path), f"{so_path} is not a file."

def test_secure_py_exists_and_uses_ctypes():
    """Check that secure.py exists, imports ctypes, and loads the shared object."""
    py_path = "/home/user/calculator/secure.py"
    assert os.path.exists(py_path), f"Python script {py_path} does not exist."
    assert os.path.isfile(py_path), f"{py_path} is not a file."

    with open(py_path, "r") as f:
        content = f.read()

    assert "import ctypes" in content or "from ctypes import" in content, f"{py_path} does not seem to import ctypes."
    assert "libsafe_eval.so" in content, f"{py_path} does not seem to load the libsafe_eval.so shared object."