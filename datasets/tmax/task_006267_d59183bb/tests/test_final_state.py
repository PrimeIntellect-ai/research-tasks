# test_final_state.py

import os
import pytest

def test_result_file_exists():
    """Check if the result file exists."""
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Result file is missing at {result_path}"
    assert os.path.isfile(result_path), f"{result_path} is not a file"

def test_result_content():
    """Check if the result file contains the correct output."""
    result_path = "/home/user/result.txt"
    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected = "42,1337,2"
    assert content == expected, f"Expected result '{expected}', but got '{content}'"

def test_rust_project_exists():
    """Check if the Rust project directory and files exist."""
    project_path = "/home/user/seq_match"
    assert os.path.isdir(project_path), f"Rust project directory missing at {project_path}"

    cargo_toml = os.path.join(project_path, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing at {cargo_toml}"

    main_rs = os.path.join(project_path, "src", "main.rs")
    assert os.path.isfile(main_rs), f"main.rs missing at {main_rs}"

def test_rayon_dependency():
    """Check if rayon is added as a dependency in Cargo.toml."""
    cargo_toml = "/home/user/seq_match/Cargo.toml"
    with open(cargo_toml, 'r') as f:
        content = f.read()

    assert "rayon" in content, "The 'rayon' crate is missing from Cargo.toml"