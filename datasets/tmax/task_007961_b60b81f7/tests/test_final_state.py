# test_final_state.py

import os
import pytest

def test_parsed_ips_exists_and_correct():
    output_path = "/home/user/forensics/parsed_ips.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did you run the compiled parser?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ips = [
        "192.168.1.100",
        "10.5.5.5",
        "255.255.255.255",
        "192.168.111.222",
        "172.16.0.1"
    ]

    assert len(lines) == len(expected_ips), f"Expected {len(expected_ips)} IPs, but found {len(lines)} in {output_path}."

    for i, (actual, expected) in enumerate(zip(lines, expected_ips)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'. The malformed IP might not be truncated correctly."

def test_parser_executable_exists():
    executable_path = "/home/user/forensics/parser"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} is missing. Did you compile parser.c?"
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_parser_c_fixed():
    parser_path = "/home/user/forensics/parser.c"
    assert os.path.isfile(parser_path), f"Source file {parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    # The original buggy condition was "i <= 15". 
    # The fix should prevent i from reaching 15 inside the loop body, or handle it correctly.
    # While there are multiple ways to fix it (e.g. i < 15, i <= 14), we can just check that the original bug is gone.
    assert "i <= 15" not in content, "The original off-by-one bug (i <= 15) is still present in parser.c."