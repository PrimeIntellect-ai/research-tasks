# test_final_state.py

import os
import re

def test_files_exist():
    """Verify that all required files exist."""
    required_files = [
        "/home/user/oscillator.c",
        "/home/user/timeseries.csv",
        "/home/user/analyze.c",
        "/home/user/report.txt"
    ]
    for filepath in required_files:
        assert os.path.isfile(filepath), f"Required file {filepath} is missing."

def test_timeseries_format():
    """Verify that timeseries.csv has 1001 lines with t,y format."""
    filepath = "/home/user/timeseries.csv"
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 1001, f"Expected exactly 1001 lines in timeseries.csv, but found {len(lines)}."

    # Check the first and last line to ensure it's roughly correct
    first_line = lines[0].split(',')
    assert len(first_line) == 2, "Each line in timeseries.csv must have exactly two comma-separated values."

    t0 = float(first_line[0])
    y0 = float(first_line[1])
    assert abs(t0 - 0.0) < 1e-6, "First t value should be 0.00"
    assert abs(y0 - 1.0) < 1e-6, "First y value should be 1.00"

def test_report_content():
    """Verify the contents of report.txt match the expected format and values."""
    filepath = "/home/user/report.txt"
    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_freq = r"Dominant Frequency:\s*1\.5800\s*Hz"
    expected_ci = r"Mean CI:\s*\[-0\.0101,\s*0\.0267\]"

    assert re.search(expected_freq, content), (
        f"Could not find the expected Dominant Frequency in {filepath}. "
        f"Expected 'Dominant Frequency: 1.5800 Hz'. File content:\n{content}"
    )

    assert re.search(expected_ci, content), (
        f"Could not find the expected Mean CI in {filepath}. "
        f"Expected 'Mean CI: [-0.0101, 0.0267]'. File content:\n{content}"
    )