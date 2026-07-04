# test_final_state.py

import os
import pytest
import stat

def test_c_source_code_exists():
    source_file = "/home/user/processor.c"
    assert os.path.isfile(source_file), f"C source file {source_file} does not exist."

def test_executable_exists_and_is_executable():
    executable_file = "/home/user/processor"
    assert os.path.isfile(executable_file), f"Executable {executable_file} does not exist."

    # Check if the file is executable
    st = os.stat(executable_file)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {executable_file} is not executable."

def test_vwas_report_correctness():
    report_file = "/home/user/vwas_report.csv"
    assert os.path.isfile(report_file), f"Output report {report_file} does not exist."

    with open(report_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "symbol,vwas",
        "AAPL,0.0800",
        "MSFT,0.1250",
        "TSLA,0.5000"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {report_file}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."