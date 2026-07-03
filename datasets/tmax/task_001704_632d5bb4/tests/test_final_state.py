# test_final_state.py

import os
import pytest

def test_resolution_log_exists_and_correct():
    log_path = "/home/user/resolution.log"

    assert os.path.isfile(log_path), f"The resolution log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "MALICIOUS_FILE: profile.gif",
        "PIN: 8426",
        "PORT: 44322"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, found {len(lines)}."

    for expected, actual in zip(expected_lines, lines):
        assert actual == expected, f"Expected line '{expected}', but found '{actual}' in {log_path}."