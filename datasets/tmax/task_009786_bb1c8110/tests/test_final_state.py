# test_final_state.py

import os
import pytest

def test_rust_file_exists():
    """Verify that the Rust source file was created."""
    rust_file = "/home/user/path_optimizer.rs"
    assert os.path.isfile(rust_file), f"Rust source file {rust_file} is missing. You must create the Rust program."

def test_optimized_path_exists_and_correct():
    """Verify that the output file exists and contains the correct shortest path."""
    output_file = "/home/user/optimized_path.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you run the Rust program?"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    expected_path = "NODE_START,B,NODE_END"

    assert content == expected_path, (
        f"The computed path in {output_file} is incorrect.\n"
        f"Expected: '{expected_path}'\n"
        f"Got: '{content}'\n"
        "Ensure you are properly filtering out non-ACTIVE edges (like MAINTENANCE and OFFLINE) "
        "and computing the shortest path by total cost."
    )