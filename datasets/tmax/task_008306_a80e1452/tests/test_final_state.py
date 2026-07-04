# test_final_state.py

import os
import pytest

def test_etl_script_exists():
    script_path = "/home/user/etl_pipeline.py"
    assert os.path.isfile(script_path), f"ETL script not found at {script_path}"

def test_report_exists():
    report_path = "/home/user/output/report.md"
    assert os.path.isfile(report_path), f"Output report not found at {report_path}"

def test_report_content():
    report_path = "/home/user/output/report.md"
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The template header should be present
    assert "# Daily Event Report" in content, "Report is missing the required header."
    assert "We processed the following unique events today:" in content, "Report is missing the introductory text."

    # Expected cleaned and deduplicated messages in order
    expected_messages = [
        "System started successfully ✓",
        "Error encountered: ? unknown module",
        "User login: admin",
        "Cache flushed",
        "Warning: ? invalid token",
        "User logout: admin"
    ]

    for msg in expected_messages:
        assert f"* {msg}" in content, f"Expected message '{msg}' not found in the report."

    # Check for duplicates or unprocessed invalid sequences
    assert "\\uZZZZ" not in content, "Unprocessed invalid unicode sequence \\uZZZZ found in report."
    assert "\\uG123" not in content, "Unprocessed invalid unicode sequence \\uG123 found in report."

    # Check that there are exactly 6 items in the list to ensure deduplication worked
    list_items = [line for line in content.splitlines() if line.strip().startswith("* ")]
    assert len(list_items) >= 5, "Validation checkpoint failed: There should be at least 5 unique records."

    # Ensure no duplicates in the report list
    unique_items = set(list_items)
    assert len(list_items) == len(unique_items), "Duplicate messages found in the final report."
    assert len(list_items) == 6, f"Expected exactly 6 deduplicated messages, found {len(list_items)}."