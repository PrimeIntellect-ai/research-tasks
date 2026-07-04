# test_final_state.py

import os
import stat
import pytest

def test_build_sh_exists():
    path = "/home/user/build.sh"
    assert os.path.isfile(path), f"File {path} is missing. You need to write a build script."

def test_shared_library_exists():
    path = "/home/user/libmathops.so"
    assert os.path.isfile(path), f"Shared library {path} is missing. Ensure your build script compiles it."

def test_processor_executable_exists():
    path = "/home/user/processor"
    assert os.path.isfile(path), f"Executable {path} is missing. Ensure your build script compiles it."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{path} is not executable."

def test_output_txt_content():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} is missing. Ensure you run the compiled processor."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "17.30",
        "15.87",
        "15.10",
        "12.57"
    ]

    assert lines == expected, f"Content of {path} does not match the expected descending moving averages. Got {lines}, expected {expected}."