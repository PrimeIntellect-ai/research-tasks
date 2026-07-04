# test_final_state.py

import os
import pytest

def test_results_file_exists():
    """Verify that the results directory and output file exist."""
    output_file = "/home/user/results/top_abstracts.txt"
    assert os.path.exists(output_file), f"The file {output_file} was not created."
    assert os.path.isfile(output_file), f"{output_file} is not a valid file."

def test_results_file_content():
    """Verify that the output file contains the correct top 2 document IDs in the correct order."""
    output_file = "/home/user/results/top_abstracts.txt"

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 document IDs in {output_file}, but found {len(lines)}."
    assert lines[0] == "101", f"Expected the first ID (highest Log-Odds) to be '101', got '{lines[0]}'."
    assert lines[1] == "102", f"Expected the second ID to be '102', got '{lines[1]}'."