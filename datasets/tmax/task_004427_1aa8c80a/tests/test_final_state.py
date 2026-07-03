# test_final_state.py

import os
import pytest

FINAL_REPORT_PATH = "/home/user/final_report.txt"

def test_final_report_exists():
    assert os.path.isfile(FINAL_REPORT_PATH), f"Final report file is missing at {FINAL_REPORT_PATH}"

def test_final_report_contents():
    with open(FINAL_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that template parts are preserved
    assert "=== NETWORK LATENCY REPORT ===" in content, "Report is missing the header."
    assert "Date: 2023-10-25" in content, "Report is missing the date."
    assert "------------------------------" in content, "Report is missing the separator."
    assert "==============================" in content, "Report is missing the footer."

    # Check that the placeholder was replaced
    assert "{{REPORTS}}" not in content, "The {{REPORTS}} placeholder was not replaced."

    # Check for the expected calculated means
    assert "ServerAlpha: 48.00 ms" in content, "ServerAlpha mean is incorrect or missing."
    assert "ServerBeta: 100.00 ms" in content, "ServerBeta mean is incorrect or missing."
    assert "ServerGamma: 89.15 ms" in content, "ServerGamma mean is incorrect or missing."