# test_final_state.py

import os
import pytest

def test_deadlocked_txs_output():
    output_path = "/home/user/deadlocked_txs.txt"

    assert os.path.exists(output_path), f"The output file {output_path} does not exist. Did you run the program and write the output?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    expected_lines = ["4", "5", "6", "10"]

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {output_path} does not match the expected paginated deadlocked transaction IDs.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )