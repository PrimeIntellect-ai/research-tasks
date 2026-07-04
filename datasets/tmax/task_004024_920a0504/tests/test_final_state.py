# test_final_state.py

import os
import pytest

def test_highest_cost_file_exists_and_content():
    file_path = "/home/user/highest_cost.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "S1:560", f"Expected 'S1:560' in {file_path}, but found '{content}'."

def test_rust_source_file_exists():
    file_path = "/home/user/calculate_costs.rs"
    # The task allows initializing a cargo project, but it specifically says:
    # "Write a Rust program at /home/user/calculate_costs.rs"
    assert os.path.isfile(file_path), f"Rust source file {file_path} is missing."