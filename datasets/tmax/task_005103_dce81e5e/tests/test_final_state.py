# test_final_state.py

import os

def test_rust_project_exists():
    """Verify that the Rust project directory exists."""
    project_dir = "/home/user/ols_pipeline"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}. Is it a valid Rust project?"

def test_coefficients_output():
    """Verify that the coefficients.txt file exists and contains the correct values."""
    output_file = "/home/user/output/coefficients.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 coefficients in {output_file}, but found {len(lines)}."

    expected_coefficients = ["2.0000", "3.0000", "1.0000"]

    for i, (actual, expected) in enumerate(zip(lines, expected_coefficients)):
        assert actual == expected, f"Coefficient {i} mismatch: expected {expected}, got {actual}."