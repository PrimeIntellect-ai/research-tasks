# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    """Test that the Rust project was initialized."""
    cargo_toml = "/home/user/route-compiler/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Rust project not found. Expected Cargo.toml at {cargo_toml}"

def test_merged_txt_content():
    """Test that merged.txt is generated correctly according to the processing rules."""
    merged_file = "/home/user/merged.txt"
    assert os.path.isfile(merged_file), f"Output file {merged_file} does not exist."

    expected_lines = [
        "DELETE /api/data [] -> api_delete (Weight: 100)",
        "GET /api/data [filter] -> api_handler (Weight: 50)",
        "POST /login [method] -> legacy_login (Weight: 20)",
        "GET /home [lang] -> home_handler (Weight: 10)"
    ]

    with open(merged_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {merged_file} do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_diff_txt_content():
    """Test that diff.txt is generated correctly according to diffing rules."""
    diff_file = "/home/user/diff.txt"
    assert os.path.isfile(diff_file), f"Output file {diff_file} does not exist."

    expected_lines = [
        "MODIFIED: GET /api/data",
        "ADDED: POST /login",
        "REMOVED: PUT /upload"
    ]

    with open(diff_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {diff_file} do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )