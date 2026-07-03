# test_final_state.py

import os
import math

def test_report_exists_and_correct():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Expected report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # We expect exactly two lines or at least checking the keys.
    # Let's check for the exact expected strings to be robust.

    slope_line_found = False
    status_line_found = False

    for line in lines:
        if line.startswith("SLOPE:"):
            slope_line_found = True
            assert line == "SLOPE: 2.99", f"Expected SLOPE: 2.99, but got '{line}'"
        elif line.startswith("STATUS:"):
            status_line_found = True
            assert line == "STATUS: STABLE_CUBIC", f"Expected STATUS: STABLE_CUBIC, but got '{line}'"

    assert slope_line_found, "The 'SLOPE: <value>' line is missing from the report."
    assert status_line_found, "The 'STATUS: <status>' line is missing from the report."