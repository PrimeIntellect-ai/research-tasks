# test_final_state.py

import os
import pytest

def test_audit_list_exists_and_correct():
    output_file = '/home/user/audit_list.txt'
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist. Did your C++ program run and generate it?"

    expected_lines = [
        "storage-C: 2",
        "storage-D: 2",
        "storage-W: 3",
        "storage-Y: 3",
        "storage-Z: 4",
        "storage-Omega: 5"
    ]

    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {output_file} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )