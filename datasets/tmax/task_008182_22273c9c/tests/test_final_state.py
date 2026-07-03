# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    """Verify that the Rust project was created at the expected location."""
    project_dir = "/home/user/processor"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}. Is it a valid Cargo project?"

def test_cleaned_telemetry_output():
    """Verify that the output file exists and has the correct processed content."""
    output_file = "/home/user/cleaned_telemetry.csv"

    assert os.path.isfile(output_file), f"Output file {output_file} was not generated."

    expected_content = """timestamp,rolling_avg
1700000100,10.00
1700000101,11.00
1700000102,11.33
1700000103,12.00
1700000104,13.00
1700000105,14.00
1700000106,15.00
1700000107,16.00"""

    with open(output_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {output_file} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )