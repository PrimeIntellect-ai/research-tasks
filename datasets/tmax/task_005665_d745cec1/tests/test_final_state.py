# test_final_state.py

import os
import pytest

def test_c_source_exists():
    source_path = "/home/user/process_results.c"
    assert os.path.isfile(source_path), f"Missing C source code file: {source_path}"

def test_executable_exists():
    exec_path = "/home/user/process_results"
    assert os.path.isfile(exec_path), f"Missing executable file: {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File {exec_path} is not executable"

def test_report_tsv_content():
    report_path = "/home/user/report.tsv"
    assert os.path.isfile(report_path), f"Missing report file: {report_path}"

    expected_lines = [
        "101\t201\tAn overview of modern artificial intelligence and its roots.",
        "101\t202\tThis paper reevaluates the concept of the Turing machine in the 21st century.",
        "102\t202\tThis paper reevaluates the concept of the Turing machine in the 21st century.",
        "102\t203\tA comprehensive history of computing from the 1930s to today."
    ]

    with open(report_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip('\n') for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report.tsv, but found {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1} in report.tsv.\nExpected: {expected}\nActual: {actual}"