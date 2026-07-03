# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    """Verify that the Rust project was created with Cargo."""
    cargo_toml_path = "/home/user/etl/pipeline/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"Rust project not found. Expected Cargo.toml at {cargo_toml_path}"
    assert os.path.isfile(cargo_toml_path), f"Path {cargo_toml_path} is not a file."

def test_output_file_exists():
    """Verify that the output JSON file exists."""
    output_file = "/home/user/etl/shortest_path.json"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

def test_shortest_path_result():
    """Verify that the shortest path in the JSON file is correct."""
    output_file = "/home/user/etl/shortest_path.json"

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    expected_path = ["Product_Omega", "Subassembly_B", "Component_Y", "Raw_Silicon"]

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."
    assert data == expected_path, f"Incorrect shortest path. Expected {expected_path}, but got {data}."