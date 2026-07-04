# test_final_state.py

import os
import pytest

def test_curate_c_exists():
    assert os.path.isfile('/home/user/curate.c'), "/home/user/curate.c is missing. You must write the C program."

def test_curation_report_exists():
    assert os.path.isfile('/home/user/curation_report.txt'), "/home/user/curation_report.txt is missing. You must generate the report."

def test_curation_report_contents():
    expected_lines = [
        "[ACCEPT] bin/server (Arch: 0x3e)",
        "[ACCEPT] lib/module.so (Arch: 0x28)",
        "[REJECT] ../../../etc/passwd (Path Traversal)",
        "[REJECT] usr/bin/../lib/test (Path Traversal)"
    ]

    with open('/home/user/curation_report.txt', 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in the report, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'."