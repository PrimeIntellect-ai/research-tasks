# test_final_state.py

import os
import re
import pytest

REPORT_PATH = "/home/user/report.txt"
SPECTRUM_PATH = "/home/user/spectrum.csv"

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} does not exist."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_spectrum_exists():
    assert os.path.exists(SPECTRUM_PATH), f"{SPECTRUM_PATH} does not exist."
    assert os.path.isfile(SPECTRUM_PATH), f"{SPECTRUM_PATH} is not a file."

def test_report_content():
    with open(REPORT_PATH, "r") as f:
        content = f.read()

    assert "Dominant Frequency Bin: 42" in content, "Incorrect dominant frequency bin in report.txt. Expected 42."

    match = re.search(r"Mean 95% CI:\s*\[([\d\.]+),\s*([\d\.]+)\]", content)
    assert match is not None, "Mean 95% CI format is incorrect or missing in report.txt."

    lower = float(match.group(1))
    upper = float(match.group(2))

    assert 14.85 < lower < 15.00, f"Lower bound {lower} is out of expected range (14.85, 15.00)."
    assert 15.10 < upper < 15.25, f"Upper bound {upper} is out of expected range (15.10, 15.25)."

def test_spectrum_content():
    with open(SPECTRUM_PATH, "r") as f:
        lines = f.readlines()

    # Bins 0 to 511 means exactly 512 lines, or more if there's a header.
    assert len(lines) >= 512, f"{SPECTRUM_PATH} does not contain enough bins (expected at least 512 lines)."

    # Check that it has some valid numbers
    valid_lines = 0
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 2:
            try:
                float(parts[0])
                float(parts[1])
                valid_lines += 1
            except ValueError:
                pass

    assert valid_lines >= 512, f"{SPECTRUM_PATH} does not contain at least 512 valid 'bin,magnitude' lines."