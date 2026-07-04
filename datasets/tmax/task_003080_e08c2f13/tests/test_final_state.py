# test_final_state.py
import os
import json
import math
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = "/home/user/pipeline.sh"
    result_path = "/home/user/result.json"

    # Remove result.json if it exists to ensure the script generates it
    if os.path.exists(result_path):
        os.remove(result_path)

    # Execute the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}. stderr: {result.stderr}"

    # Check if result.json was created
    assert os.path.isfile(result_path), f"The pipeline script did not generate {result_path}."

    # Read and verify the JSON output
    with open(result_path, 'r') as f:
        try:
            coeffs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} does not contain valid JSON.")

    assert isinstance(coeffs, list), f"Expected a JSON array in {result_path}, got {type(coeffs)}."
    assert len(coeffs) == 3, f"Expected exactly 3 coefficients in {result_path}, got {len(coeffs)}."

    expected = [0.14000000, 0.94142857, 1.00714286]

    for c, e in zip(coeffs, expected):
        assert isinstance(c, (int, float)), f"Coefficient {c} is not a number."
        assert math.isclose(c, e, rel_tol=1e-3, abs_tol=1e-3), \
            f"Mismatch in coefficients: got {coeffs}, expected approximately {expected}."

def test_rust_project_structure():
    cargo_toml = "/home/user/polyfit/Cargo.toml"
    src_main = "/home/user/polyfit/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} does not exist."
    assert os.path.isfile(src_main), f"Rust source file {src_main} does not exist."