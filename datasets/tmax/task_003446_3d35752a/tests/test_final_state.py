# test_final_state.py

import os
import pytest

def get_collatz_steps(n):
    count = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        count += 1
    return count

def test_recovered_password():
    password_file = "/home/user/recovered_password.txt"
    assert os.path.exists(password_file), f"File {password_file} does not exist."

    with open(password_file, "r") as f:
        content = f.read().strip()

    expected_password = "h4ckth3m4th!99"
    assert content == expected_password, f"Recovered password is incorrect. Expected '{expected_password}', got '{content}'."

def test_collatz_output():
    output_file = "/home/user/collatz_20.txt"
    assert os.path.exists(output_file), f"File {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 20, f"Expected 20 lines of output in {output_file}, but found {len(lines)}."

    for i in range(1, 21):
        expected_steps = get_collatz_steps(i)
        expected_line = f"{i}: {expected_steps}"
        actual_line = lines[i-1]
        assert actual_line == expected_line, f"Line {i} is incorrect. Expected '{expected_line}', got '{actual_line}'."