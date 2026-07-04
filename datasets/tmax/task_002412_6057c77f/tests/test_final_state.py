# test_final_state.py

import os
import pytest

def test_clean_data_file():
    """Test that clean_data.csv exists and has the correct content."""
    file_path = '/home/user/clean_data.csv'
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    expected_content = """10.0,2.0,3.5
5.0,2.5,1.0
0.0,0.0,0.0
8.0,4.0,2.0
-3.0,1.5,0.5
2.0,2.0,2.0"""

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} is incorrect."

def test_rust_project_structure():
    """Test that the Rust project was initialized correctly."""
    cargo_toml = '/home/user/data_analyzer/Cargo.toml'
    main_rs = '/home/user/data_analyzer/src/main.rs'

    assert os.path.isfile(cargo_toml), f"Rust project Cargo.toml missing at {cargo_toml}"
    assert os.path.isfile(main_rs), f"Rust project main.rs missing at {main_rs}"

    with open(cargo_toml, 'r') as f:
        content = f.read()

    assert 'ndarray' in content, "Cargo.toml is missing the 'ndarray' dependency."
    assert 'csv' in content, "Cargo.toml is missing the 'csv' dependency."

def test_trace_output():
    """Test that trace.txt exists and has the correct calculated value."""
    file_path = '/home/user/trace.txt'
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "256.00", f"Content of {file_path} is incorrect. Expected '256.00', got '{content}'."