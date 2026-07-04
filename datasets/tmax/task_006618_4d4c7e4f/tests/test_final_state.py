# test_final_state.py
import os
import pytest

def test_debug_report_exists_and_correct():
    report_path = "/home/user/debug_report.txt"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 non-empty lines in {report_path}, found {len(lines)}."
    assert lines[0] == "42", f"Expected sequence number '42' on line 1, found '{lines[0]}'."
    assert lines[1] == "MALFORMED_DATA_FRAG", f"Expected payload 'MALFORMED_DATA_FRAG' on line 2, found '{lines[1]}'."