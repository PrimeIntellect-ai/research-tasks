# test_final_state.py

import os
import pytest

def test_report_txt_content():
    """Test that the report.txt file contains the exact expected content."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    expected_content = (
        "Total Valid Changes: 3\n"
        "Total Cost Impact: 170\n"
        "Masked Authors:\n"
        "- ***@acme.corp\n"
        "- ***@acme.corp\n"
        "- ***@acme.corp"
    )

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content.strip(), f"Content of {report_path} does not match the expected output."

def test_cron_txt_content():
    """Test that the cron.txt file contains the correct schedule and command."""
    cron_path = "/home/user/cron.txt"
    assert os.path.isfile(cron_path), f"File {cron_path} does not exist."

    with open(cron_path, "r") as f:
        content = f.read()

    assert "0 * * * *" in content, f"File {cron_path} does not contain the correct cron schedule '0 * * * *'."
    assert "process.go" in content, f"File {cron_path} does not contain the command to run 'process.go'."