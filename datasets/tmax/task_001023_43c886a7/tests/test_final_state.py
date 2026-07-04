# test_final_state.py

import os

def test_total_print_time_file_exists():
    """Check if the output file exists."""
    filepath = "/home/user/total_print_time.txt"
    assert os.path.exists(filepath), f"Output file {filepath} does not exist."
    assert os.path.isfile(filepath), f"Path {filepath} is not a file."

def test_total_print_time_value():
    """Verify that the total print time is calculated correctly."""
    filepath = "/home/user/total_print_time.txt"
    assert os.path.exists(filepath), f"Output file {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "1100", f"Expected total print time to be 1100, but got '{content}'."