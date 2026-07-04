# test_final_state.py
import os
import pytest

def test_rust_source_exists():
    source_file = "/home/user/find_k.rs"
    assert os.path.isfile(source_file), f"The Rust source file {source_file} is missing."

def test_optimal_k_output():
    output_file = "/home/user/optimal_k.txt"
    assert os.path.isfile(output_file), f"The output file {output_file} is missing."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "0.34", f"Expected {output_file} to contain exactly '0.34', but found '{content}'."