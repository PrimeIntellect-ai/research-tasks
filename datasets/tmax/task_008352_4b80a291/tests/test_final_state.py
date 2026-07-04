# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    """Check if the Rust project directory exists."""
    project_dir = "/home/user/svd_analyzer"
    assert os.path.exists(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isdir(project_dir), f"{project_dir} is not a directory."
    assert os.path.exists(os.path.join(project_dir, "Cargo.toml")), "Cargo.toml not found in the Rust project."

def test_sv_diff_output():
    """Check if the final output file exists and has the correct contents."""
    output_file = "/home/user/sv_diff.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_file}, but found {len(lines)}."

    expected_values = ["0.46", "0.21", "0.00"]

    for i, (actual, expected) in enumerate(zip(lines, expected_values)):
        assert actual.strip() == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual.strip()}'."