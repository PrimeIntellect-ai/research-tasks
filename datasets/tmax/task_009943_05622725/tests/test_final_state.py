# test_final_state.py

import os
import pytest

def test_report_csv_exists_and_content():
    report_path = "/home/user/report.csv"
    assert os.path.isfile(report_path), f"File {report_path} was not generated."

    expected_content = """account_id,name,max_balance
1,Root,5000
2,Branch_A,2000
3,Branch_B,2000
6,Deep_Leaf,1700
4,Leaf_A1,1500"""

    with open(report_path, "r") as f:
        content = f.read().strip()

    # Split into lines to compare robustly, ignoring trailing/leading whitespace per line
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {report_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{content}"
    )

def test_analyze_cpp_exists():
    cpp_path = "/home/user/analyze.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."