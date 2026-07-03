# test_final_state.py
import os
import pytest

def test_final_surveys_exists():
    file_path = '/home/user/final_surveys.csv'
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_final_surveys_content():
    file_path = '/home/user/final_surveys.csv'
    expected_content = [
        "user_id,age,question_id,normalized_text",
        "1,25,q1_response,great product",
        "1,25,q2_response,too expensive",
        "2,34,q1_response,needs work",
        "2,34,q3_response,no comment",
        "3,45,q2_response,okay",
        "3,45,q3_response,very badexperience",
        "4,29,q1_response,awesome",
        "4,29,q2_response,loved it",
        "4,29,q3_response,yes"
    ]

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_content), f"Expected {len(expected_content)} lines in final_surveys.csv, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_content)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'"

def test_pipeline_log_exists():
    log_path = '/home/user/pipeline.log'
    assert os.path.exists(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

def test_pipeline_log_content():
    log_path = '/home/user/pipeline.log'
    with open(log_path, 'r') as f:
        content = f.read()

    expected_messages = [
        "Pipeline started",
        "Melted data: 15 rows",
        "Cleaned data: 9 rows",
        "Pipeline completed"
    ]

    for msg in expected_messages:
        assert msg in content, f"Expected log message '{msg}' not found in {log_path}"