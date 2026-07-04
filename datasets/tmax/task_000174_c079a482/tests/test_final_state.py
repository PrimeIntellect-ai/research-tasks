# test_final_state.py

import os
import pytest

def test_extracted_records_file():
    extracted_path = "/home/user/extracted_records.txt"
    assert os.path.isfile(extracted_path), f"Extracted records missing: {extracted_path}"

    with open(extracted_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1699999999 45.5",
        "1700000050 10.2",
        "1700000060 15.5",
        "1700000070 20.1",
        "1700000080 30.0"
    ]

    assert lines == expected_lines, f"Extracted records incorrect.\nExpected: {expected_lines}\nGot: {lines}"

def test_bad_commit_file():
    truth_path = "/home/user/.truth_bad_commit"
    student_path = "/home/user/bad_commit.txt"

    assert os.path.isfile(truth_path), f"Truth file missing: {truth_path}"
    assert os.path.isfile(student_path), f"Student file missing: {student_path}"

    with open(truth_path, "r") as f:
        truth_hash = f.read().strip()

    with open(student_path, "r") as f:
        student_hash = f.read().strip()

    assert student_hash == truth_hash, f"Expected bad commit hash {truth_hash}, but got {student_hash}"

def test_final_report_file():
    report_path = "/home/user/final_report.txt"
    assert os.path.isfile(report_path), f"Final report missing: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Processed: 4 records\nAverage Latency: 18.950 ms"

    assert content == expected_content, f"Final report content incorrect.\nExpected:\n{expected_content}\nGot:\n{content}"