# test_final_state.py

import os
import pytest

def test_critical_archive_contents():
    archive_path = "/home/user/critical_archive.txt"
    assert os.path.isfile(archive_path), f"Output file {archive_path} does not exist."

    with open(archive_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "CRITICAL [REDACTED] Disk full",
        "CRITICAL [REDACTED] Memory out of bounds"
    ]

    assert len(lines) == 2, f"Expected exactly 2 lines in {archive_path}, but found {len(lines)}. Contents: {lines}"

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {archive_path}. Contents: {lines}"

def test_last_run_stamp_updated():
    stamp_path = "/home/user/last_run.stamp"
    assert os.path.isfile(stamp_path), f"File {stamp_path} does not exist."

    with open(stamp_path, "r") as f:
        content = f.read().strip()

    try:
        new_stamp = float(content)
    except ValueError:
        pytest.fail(f"Content of {stamp_path} is not a valid float: '{content}'")

    assert new_stamp > 1700000000.0, f"Expected {stamp_path} to be updated to a timestamp > 1700000000.0, but got {new_stamp}"