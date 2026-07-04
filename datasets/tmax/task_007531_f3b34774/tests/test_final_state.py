# test_final_state.py

import os
import pytest

def test_cpp_file_exists():
    """Check if the C++ source file was created."""
    cpp_file = "/home/user/pinns_data/generate_data.cpp"
    assert os.path.isfile(cpp_file), f"The C++ source file {cpp_file} does not exist."

def test_stats_file_exists():
    """Check if the stats.txt file was generated."""
    stats_file = "/home/user/pinns_data/stats.txt"
    assert os.path.isfile(stats_file), f"The output file {stats_file} does not exist. Did you run your program?"

def test_stats_file_contents():
    """Verify the contents of stats.txt."""
    stats_file = "/home/user/pinns_data/stats.txt"
    if not os.path.isfile(stats_file):
        pytest.fail(f"{stats_file} is missing.")

    with open(stats_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {stats_file}, found {len(lines)}."

    # Check line 1
    assert lines[0] == "MSE: 0.0100", f"Expected first line to be 'MSE: 0.0100', but got '{lines[0]}'."

    # Check line 2
    assert lines[1] == "H0: Accepted", f"Expected second line to be 'H0: Accepted', but got '{lines[1]}'."