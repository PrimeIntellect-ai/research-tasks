# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    pipeline_dir = "/home/user/pipeline"
    assert os.path.isdir(pipeline_dir), f"Directory {pipeline_dir} is missing. Did you initialize the Rust project?"

    cargo_toml = os.path.join(pipeline_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"File {cargo_toml} is missing. Ensure the project is a valid Rust Cargo project."

def test_posterior_json_exists_and_correct():
    posterior_file = "/home/user/posterior.json"
    assert os.path.isfile(posterior_file), f"File {posterior_file} is missing. Did you generate the output?"

    with open(posterior_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {posterior_file} is not a valid JSON file.")

    assert "alpha" in data, f"'alpha' key missing in {posterior_file}"
    assert "beta" in data, f"'beta' key missing in {posterior_file}"

    assert isinstance(data["alpha"], int), "'alpha' must be an integer"
    assert isinstance(data["beta"], int), "'beta' must be an integer"

    assert data["alpha"] == 3, f"Expected alpha to be 3, got {data['alpha']}"
    assert data["beta"] == 2, f"Expected beta to be 2, got {data['beta']}"