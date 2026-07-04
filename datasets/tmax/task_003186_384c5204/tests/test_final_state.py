# test_final_state.py

import os
import math
import pytest

def get_expected_max_error():
    max_err = 0.0
    for n in range(101):
        t = n * 0.1
        y_num = 1.0 * (0.95 ** n)
        y_exact = math.exp(-0.5 * t)
        err = abs(y_num - y_exact)
        if err > max_err:
            max_err = err
    return f"{max_err:.6f}"

def test_rust_project_exists():
    """Check that the Rust project directory and Cargo.toml exist."""
    project_dir = "/home/user/ode_validator"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}."

def test_max_error_file_content():
    """Check that the output file exists and contains the correct maximum absolute error."""
    output_file = "/home/user/max_error.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    expected = get_expected_max_error()
    assert content == expected, f"Incorrect max error. Expected '{expected}', got '{content}'."