# test_final_state.py

import os
import math
import pytest

def get_sum_of_proper_divisors(n):
    if n <= 1:
        return 0
    s = 1
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            s += i
            if i != n // i:
                s += n // i
    return s

def test_solution_file_exists():
    """Test that the solution.txt file exists."""
    file_path = "/home/user/ticket_4092/solution.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. You must create the solution file."

def test_solution_contents():
    """Test that the solution.txt file contains the correct output."""
    file_path = "/home/user/ticket_4092/solution.txt"

    # The numbers encoded in the PCAP file
    expected_numbers = [28, 36, 8128, 100]
    expected_lines = [f"{n}: {get_sum_of_proper_divisors(n)}" for n in expected_numbers]

    with open(file_path, "r") as f:
        content = f.read()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in solution.txt, but found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} is incorrect.\n"
            f"Expected: '{expected}'\n"
            f"Found: '{actual}'"
        )