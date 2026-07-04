# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    """Verify that the Rust project was created in the correct directory."""
    project_dir = "/home/user/sensor_parser"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory missing at {project_dir}"
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing at {cargo_toml}"

def test_extracted_log_contents():
    """Verify that the output log file exists and contains the correct extracted records."""
    log_path = "/home/user/extracted_sensor_42.log"
    assert os.path.isfile(log_path), f"Output log file is missing at {log_path}"

    with open(log_path, "r") as f:
        # Read lines and strip trailing newlines for comparison
        lines = [line.strip("\r\n") for line in f.readlines()]

    # Remove any empty trailing lines that might have been caused by a trailing newline
    if lines and lines[-1] == "":
        lines.pop()

    expected_lines = [
        "Timestamp: 1600000050, Payload: aabbccdd",
        "Timestamp: 1600000100, Payload: 1122334455",
        "Timestamp: 1600000200, Payload: "
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but found {len(lines)} in {log_path}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: '{expected}'\nGot:      '{actual}'"