# test_final_state.py
import os
import re

def test_recovery_report_exists():
    """Check if the recovery report was generated."""
    report_file = "/home/user/recovery_report.txt"
    assert os.path.isfile(report_file), f"The file {report_file} does not exist."

def test_recovery_report_content():
    """Check if the recovery report contains the correct values."""
    report_file = "/home/user/recovery_report.txt"
    with open(report_file, "r") as f:
        content = f.read().strip()

    expected_txid_line = "Corrupted TxID: 3"
    expected_total_line = "Recovered Total: 500"

    assert expected_txid_line in content, "The report does not contain the correct Corrupted TxID or the format is incorrect."
    assert expected_total_line in content, "The report does not contain the correct Recovered Total or the format is incorrect."

    # Check exact format if needed
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    assert len(lines) >= 2, "The report should contain at least two lines."
    assert lines[0] == expected_txid_line, f"Expected first line to be '{expected_txid_line}', got '{lines[0]}'."
    assert lines[1] == expected_total_line, f"Expected second line to be '{expected_total_line}', got '{lines[1]}'."