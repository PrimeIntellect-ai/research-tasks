# test_final_state.py

import os
import pytest

def test_report_file_exists():
    """Check that the output report file has been created."""
    file_path = "/home/user/report.txt"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_report_file_contents():
    """Check that the output report has the correct format and calculations."""
    file_path = "/home/user/report.txt"

    expected_contents = (
        "Sensor S1:\n"
        "- Max 3-Period SMA: 58.00\n"
        "- Final 3-Period SMA: 53.00\n"
        "\n"
        "Sensor S2:\n"
        "- Max 3-Period SMA: 22.67\n"
        "- Final 3-Period SMA: 22.67\n"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        actual_contents = f.read()

    # We strip trailing whitespace to be slightly forgiving about EOF newlines, 
    # but the internal newlines must match exactly.
    assert actual_contents.strip() == expected_contents.strip(), (
        f"Contents of {file_path} do not match the expected report.\n"
        f"Expected:\n{expected_contents}\n"
        f"Got:\n{actual_contents}"
    )

    # Also verify the exact trailing blank line requirement if possible
    assert actual_contents.endswith("\n\n") or actual_contents.endswith("22.67\n\n") or "\n\nSensor S2" in actual_contents, \
        "Ensure there is a blank line after each sensor block as requested."