# test_final_state.py

import os
import json
import pytest

def test_cracked_json_exists_and_correct():
    path = "/home/user/cracked.json"
    assert os.path.isfile(path), f"Expected file {path} does not exist. The student must output the cracked credentials to this file."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON. Ensure the output is properly formatted.")

    expected_data = {
        "alice": "sunshine",
        "charlie": "dragon"
    }

    assert data == expected_data, f"Contents of {path} do not match the expected cracked credentials. Expected {expected_data}, but got {data}."

def test_cargo_project_initialized():
    cargo_toml_path = "/home/user/cracker/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Expected Cargo project at /home/user/cracker, but {cargo_toml_path} does not exist."