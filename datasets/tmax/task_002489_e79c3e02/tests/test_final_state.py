# test_final_state.py
import os
import re
import stat
import pytest

PROJECT_DIR = "/home/user/project"

def test_directory_structure():
    expected_dirs = ["src", "cmd", "lib", "bin"]
    for d in expected_dirs:
        dir_path = os.path.join(PROJECT_DIR, d)
        assert os.path.isdir(dir_path), f"Directory {dir_path} is missing."

def test_source_files_exist():
    expected_files = [
        "src/lib.c",
        "src/lib.h",
        "src/magic.s",
        "cmd/main.go"
    ]
    for f in expected_files:
        file_path = os.path.join(PROJECT_DIR, f)
        assert os.path.isfile(file_path), f"Source file {file_path} is missing."

def test_c_bug_fixed():
    lib_c_path = os.path.join(PROJECT_DIR, "src/lib.c")
    assert os.path.isfile(lib_c_path), f"{lib_c_path} is missing."
    with open(lib_c_path, 'r') as f:
        content = f.read()

    # The original file had `for(int i = 0; i <= 10; i++)`
    # We should ensure the out-of-bounds read is fixed.
    assert "i <= 10" not in content, "The out-of-bounds memory access bug in lib.c (i <= 10) was not fixed."

def test_compiled_artifacts():
    so_path = os.path.join(PROJECT_DIR, "lib/libmyc.so")
    app_path = os.path.join(PROJECT_DIR, "bin/app")

    assert os.path.isfile(so_path), f"Shared library {so_path} is missing."
    assert os.path.isfile(app_path), f"Go executable {app_path} is missing."

    # Check if app is executable
    st = os.stat(app_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Go binary {app_path} is not executable."

def test_output_txt():
    output_path = os.path.join(PROJECT_DIR, "output.txt")
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == "750", f"Expected output.txt to contain '750', but got '{content}'."