# test_final_state.py
import os
import pytest

def test_c_file_exists_and_contains_requirements():
    c_file_path = "/home/user/audit_extractor.c"
    assert os.path.exists(c_file_path), f"C source file {c_file_path} does not exist."
    assert os.path.isfile(c_file_path), f"{c_file_path} is not a file."

    with open(c_file_path, "r", encoding="utf-8") as f:
        content = f.read().upper()

    assert "NOT INDEXED" in content, "The SQL query in the C program must use the 'NOT INDEXED' clause."
    assert "OVER" in content, "The SQL query in the C program must use a Window Function (e.g., OVER clause)."

def test_compliance_report_contents():
    csv_path = "/home/user/compliance_report.csv"
    assert os.path.exists(csv_path), f"Compliance report {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    expected_content = (
        "E001,2023-10-15 08:32:11\n"
        "E002,2023-10-14 19:12:05\n"
        "E004,2023-10-12 12:22:22"
    )

    with open(csv_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip().replace('\r', '')

    assert actual_content == expected_content, (
        f"Contents of {csv_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )