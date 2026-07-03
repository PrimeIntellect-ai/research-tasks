# test_final_state.py

import os
import pytest
import re

def test_rust_project_structure():
    """Verify that the Rust project directory and essential files exist."""
    project_dir = "/home/user/freq_svd"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    main_rs = os.path.join(project_dir, "src", "main.rs")

    assert os.path.isdir(project_dir), f"Rust project directory not found at {project_dir}"
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}"
    assert os.path.isfile(main_rs), f"src/main.rs not found at {main_rs}"

def test_cargo_toml_dependencies():
    """Verify that nalgebra is listed as a dependency in Cargo.toml."""
    cargo_toml = "/home/user/freq_svd/Cargo.toml"

    with open(cargo_toml, "r") as f:
        content = f.read()

    assert "nalgebra" in content, "The 'nalgebra' crate is missing from Cargo.toml dependencies"

def test_output_file_contents():
    """Verify that the output.txt file exists and contains the correct largest singular value."""
    output_file = "/home/user/output.txt"

    assert os.path.isfile(output_file), f"Output file not found at {output_file}"

    with open(output_file, "r") as f:
        content = f.read().strip()

    # The expected largest singular value computed from the provided FASTA is 13.435
    expected_value = "13.435"

    assert content == expected_value, f"Expected output file to contain '{expected_value}', but found '{content}'"