# test_final_state.py
import os
import re

def test_port_directory_exists():
    assert os.path.isdir("/home/user/port"), "Directory /home/user/port does not exist."

def test_libexpr_c_no_python():
    c_file = "/home/user/port/libexpr.c"
    assert os.path.isfile(c_file), f"{c_file} does not exist."
    with open(c_file, "r") as f:
        content = f.read()
    assert "Python.h" not in content, f"{c_file} still contains Python.h or Python dependencies."
    assert "PyObject" not in content, f"{c_file} still contains PyObject references."

def test_libexpr_h_exists_and_correct():
    h_file = "/home/user/port/libexpr.h"
    assert os.path.isfile(h_file), f"{h_file} does not exist."
    with open(h_file, "r") as f:
        content = f.read()
    assert "double evaluate(const char*" in content or "double evaluate(const char *" in content, \
        f"{h_file} does not expose the correct evaluate function signature."

def test_makefile_exists():
    assert os.path.isfile("/home/user/port/Makefile"), "/home/user/port/Makefile does not exist."

def test_compiled_artifacts_exist():
    so_file = "/home/user/port/libexpr.so"
    bin_file = "/home/user/port/config_parser"
    assert os.path.isfile(so_file), f"Shared library {so_file} does not exist."
    assert os.path.isfile(bin_file), f"Executable {bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"{bin_file} is not executable."

def test_output_txt_correct():
    output_file = "/home/user/port/output.txt"
    assert os.path.isfile(output_file), f"{output_file} does not exist."

    expected_lines = [
        "Timeout=21.00",
        "MaxRetries=5.00",
        "Threshold=84.50",
        "ScaleFactor=0.25"
    ]

    with open(output_file, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {output_file} do not match the expected output."