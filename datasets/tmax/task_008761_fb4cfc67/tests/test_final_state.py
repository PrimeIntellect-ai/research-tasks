# test_final_state.py

import os
import pytest

def test_report_txt_exists_and_content():
    """Verify that the report.txt file exists and contains the correct output."""
    report_path = "/home/user/report.txt"

    # Check if the file exists
    assert os.path.exists(report_path), f"The file {report_path} was not created."
    assert os.path.isfile(report_path), f"{report_path} is not a valid file."

    # Check the content of the file
    expected_content = "User U102 had the highest total duration of 450 seconds. Their last recorded browser was Firefox."

    with open(report_path, 'r', encoding='utf-8') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {report_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{actual_content}'"
    )