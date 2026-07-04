# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    """Verify that the Rust project directory exists."""
    project_dir = "/home/user/data_prep"
    assert os.path.exists(project_dir), f"The project directory {project_dir} does not exist."
    assert os.path.isdir(project_dir), f"The path {project_dir} is not a directory."

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.exists(cargo_toml), f"Cargo.toml not found in {project_dir}."

def test_clean_norms_csv_exists():
    """Verify that the output CSV file exists."""
    file_path = "/home/user/clean_norms.csv"
    assert os.path.exists(file_path), f"The output file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_clean_norms_csv_content():
    """Verify that the output CSV file contains the correct processed data."""
    file_path = "/home/user/clean_norms.csv"

    expected_lines = [
        "timestamp,norm",
        "2023-10-01T10:00:00Z,3.0000",
        "2023-10-01T10:02:00Z,13.0000",
        "2023-10-01T10:04:00Z,1.0000",
        "2023-10-01T10:05:00Z,10.0000"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().split("\n")

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual.strip()}'."