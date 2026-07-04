# test_final_state.py

import os
import pytest

def test_report_2023_10_contents():
    """Verify the contents of the October 2023 report."""
    file_path = "/home/user/reports/report_2023-10.md"
    assert os.path.isfile(file_path), f"Expected report file {file_path} is missing."

    expected_content = (
        "## Feedback Entry\n"
        "**Date:** 2023-10-01T08:00:00Z\n"
        "**User:** c***@domain.com\n"
        "**Comment:** Standard feedback, all good!\n"
        "---\n"
        "## Feedback Entry\n"
        "**Date:** 2023-10-15T14:30:00Z\n"
        "**User:** a***@example.com\n"
        "**Comment:** This has an\n"
        "embedded newline.\n"
        "---\n"
    )

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == expected_content, f"The content of {file_path} does not match the expected output format and data."

def test_report_2023_11_contents():
    """Verify the contents of the November 2023 report."""
    file_path = "/home/user/reports/report_2023-11.md"
    assert os.path.isfile(file_path), f"Expected report file {file_path} is missing."

    expected_content = (
        "## Feedback Entry\n"
        "**Date:** 2023-11-05T09:15:00Z\n"
        "**User:** b***@test.org\n"
        "**Comment:** Invalid chars ?? here.\n"
        "---\n"
        "## Feedback Entry\n"
        "**Date:** 2023-11-20T11:00:00Z\n"
        "**User:** d***@company.net\n"
        "**Comment:** Multiple\n"
        "newlines\n"
        "???\n"
        "---\n"
    )

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == expected_content, f"The content of {file_path} does not match the expected output format and data."