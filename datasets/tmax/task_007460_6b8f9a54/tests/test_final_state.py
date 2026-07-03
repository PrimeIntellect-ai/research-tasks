# test_final_state.py

import os
import pytest

def test_makefile_exists():
    makefile_path = "/home/user/pr_review/Makefile"
    assert os.path.isfile(makefile_path), f"Expected file {makefile_path} is missing. You must create a Makefile."

def test_libdetector_so_exists():
    lib_path = "/home/user/pr_review/libdetector.so"
    assert os.path.isfile(lib_path), f"Expected shared library {lib_path} is missing. Ensure your Makefile compiles the C++ code into this shared object."

def test_scanner_executable_exists():
    scanner_path = "/home/user/pr_review/scanner"
    assert os.path.isfile(scanner_path), f"Expected executable {scanner_path} is missing. Ensure your Makefile compiles the Go code into this executable."
    assert os.access(scanner_path, os.X_OK), f"The file {scanner_path} is not executable."

def test_alerts_txt_exact_contents():
    alerts_path = "/home/user/alerts.txt"
    assert os.path.isfile(alerts_path), f"Expected output file {alerts_path} is missing. Did you run the scanner and redirect its output?"

    with open(alerts_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ids = ["2", "3", "5"]

    assert lines == expected_ids, (
        f"The contents of {alerts_path} do not match the expected output.\n"
        f"Expected: {expected_ids}\n"
        f"Actual:   {lines}\n"
        "Ensure that the C++ logic correctly identifies threats, and that the final output is sorted numerically."
    )