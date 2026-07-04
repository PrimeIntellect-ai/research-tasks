# test_final_state.py

import os
import pytest

def test_process_rs_exists():
    process_rs_path = "/home/user/process.rs"
    assert os.path.isfile(process_rs_path), f"File missing: {process_rs_path}"

def test_result_csv_exists_and_content():
    result_csv_path = "/home/user/result.csv"
    assert os.path.isfile(result_csv_path), f"File missing: {result_csv_path}"

    expected_content = (
        "username,final_score\n"
        "alice,56.12\n"
        "david,50.00\n"
        "charlie,20.00\n"
        "bob,6.93\n"
    )

    with open(result_csv_path, 'r', encoding='utf-8') as f:
        actual_content = f.read()

    # Normalize line endings to avoid issues with \r\n vs \n
    actual_content_normalized = actual_content.strip().replace('\r\n', '\n')
    expected_content_normalized = expected_content.strip()

    assert actual_content_normalized == expected_content_normalized, (
        f"Contents of {result_csv_path} do not match the expected output.\n"
        f"Expected:\n{expected_content_normalized}\n"
        f"Actual:\n{actual_content_normalized}"
    )