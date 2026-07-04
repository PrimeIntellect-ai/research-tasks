# test_final_state.py

import os
import pytest

def test_sampled_bugs_csv():
    file_path = "/home/user/sampled_bugs.csv"
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

    expected_content = """id,region,feedback
2,US,Found a massive bug in the UI
6,US,Another BUG encountered here
3,EU,Système failed completely
8,EU,Minor error on login screen
4,JP,エラー error ⚠
10,JP,Data bug detected
"""
    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Normalize line endings and strip trailing whitespace
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, f"Content of {file_path} does not match expected output."

def test_pipeline_log():
    file_path = "/home/user/pipeline.log"
    assert os.path.isfile(file_path), f"Expected log file {file_path} is missing."

    expected_content = """TOTAL_ROWS: 11
MATCHED_BUGS: 8
SAMPLED_RECORDS: 6
"""
    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, f"Content of {file_path} does not match expected output."

def test_cpp_files_exist():
    assert os.path.isfile("/home/user/process.cpp"), "Source file /home/user/process.cpp is missing."
    assert os.path.isfile("/home/user/process"), "Compiled executable /home/user/process is missing."
    assert os.access("/home/user/process", os.X_OK), "Compiled file /home/user/process is not executable."