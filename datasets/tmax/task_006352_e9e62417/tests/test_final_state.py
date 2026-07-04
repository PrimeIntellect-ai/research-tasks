# test_final_state.py

import os
import json
import subprocess
import pytest

def test_rust_project_exists():
    """Verify that the Rust project directory and Cargo.toml exist."""
    assert os.path.isdir("/home/user/etl_tester"), "Rust project directory /home/user/etl_tester does not exist."
    assert os.path.isfile("/home/user/etl_tester/Cargo.toml"), "Cargo.toml is missing in /home/user/etl_tester."

def test_rust_code_compiles_and_runs():
    """Verify that the Rust project compiles and runs successfully."""
    try:
        result = subprocess.run(
            ["cargo", "run"],
            cwd="/home/user/etl_tester",
            capture_output=True,
            text=True,
            timeout=120
        )
        assert result.returncode == 0, f"cargo run failed with return code {result.returncode}.\nStderr: {result.stderr}"
    except FileNotFoundError:
        pytest.fail("cargo command not found. Is Rust installed?")
    except subprocess.TimeoutExpired:
        pytest.fail("cargo run timed out after 120 seconds.")

def test_output_json_validity():
    """Verify the output.json file has the correct format and values."""
    output_path = "/home/user/etl_tester/output.json"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("output.json is not a valid JSON file.")

    assert "mean_frequency" in data, "Key 'mean_frequency' is missing from output.json."
    assert "standard_error" in data, "Key 'standard_error' is missing from output.json."

    mean = data["mean_frequency"]
    se = data["standard_error"]

    assert isinstance(mean, (int, float)), "mean_frequency must be a number."
    assert isinstance(se, (int, float)), "standard_error must be a number."

    # The true frequency in the generated dataset is approx 0.058
    assert 0.04 < mean < 0.08, f"Mean frequency {mean} is out of expected bounds (0.04 - 0.08)."
    assert 0.001 < se < 0.015, f"Standard error {se} is out of expected bounds (0.001 - 0.015)."