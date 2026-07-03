# test_final_state.py

import os
import json
import pytest

def test_cleaned_etl_output():
    file_path = "/home/user/cleaned_etl.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing. The C++ program failed to generate the cleaned dataset."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_lines = [
        "[2023-10-01 10:00:00] JOB-A | SEQ:100 | PAYLOAD:AlphaBeta",
        "[2023-10-01 10:01:00] JOB-A | SEQ:101 | PAYLOAD:GammaDelta",
        "[2023-10-01 10:02:00] JOB-A | SEQ:102 | PAYLOAD:EpsilonZeta",
        "[2023-10-01 10:03:00] JOB-A | SEQ:103 | PAYLOAD:EtaTheta",
        "[2023-10-01 10:07:00] JOB-A | SEQ:104 | PAYLOAD:IotaKappa",
        "[2023-10-01 10:08:00] JOB-A | SEQ:105 | PAYLOAD:LambdaMu"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, "The content of cleaned_etl.txt does not match the expected deduplicated dataset."

def test_anomaly_report_output():
    file_path = "/home/user/anomaly_report.json"
    assert os.path.exists(file_path), f"File {file_path} is missing. The C++ program failed to generate the anomaly report."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    assert "changepoint_line" in report, "Key 'changepoint_line' is missing from anomaly_report.json."
    assert "duplicates_removed" in report, "Key 'duplicates_removed' is missing from anomaly_report.json."

    assert report["changepoint_line"] == 5, f"Expected changepoint_line to be 5, but got {report['changepoint_line']}."
    assert report["duplicates_removed"] == 2, f"Expected duplicates_removed to be 2, but got {report['duplicates_removed']}."

def test_cpp_files_exist():
    cpp_file = "/home/user/cleaner.cpp"
    exe_file = "/home/user/cleaner"

    assert os.path.exists(cpp_file), f"Source file {cpp_file} is missing."
    assert os.path.exists(exe_file), f"Executable file {exe_file} is missing. Did you compile the program?"
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."