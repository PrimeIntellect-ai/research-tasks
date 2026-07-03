# test_final_state.py
import os
import json
import subprocess
import pytest
import math

def test_run_workflow_script():
    script_path = "/home/user/run_workflow.sh"
    assert os.path.exists(script_path), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute successfully. stderr: {result.stderr}"

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Results file not found: {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON")

    # Expected values computed from x^3 - cos(x) - c = 0
    expected = {
        "exp1": 1.128425,
        "exp2": 1.385234,
        "exp3": 1.804753,
        "exp4": 2.215773
    }

    for k, v in expected.items():
        assert k in results, f"Missing key '{k}' in results.json"
        assert isinstance(results[k], (int, float)), f"Value for '{k}' is not a number"
        assert abs(results[k] - v) < 1e-4, f"Value for {k} is incorrect: {results[k]} != {v} (expected)"

def test_rust_project_setup():
    cargo_path = "/home/user/solver/Cargo.toml"
    assert os.path.exists(cargo_path), f"Cargo.toml not found at {cargo_path}"

    with open(cargo_path, 'r') as f:
        cargo_contents = f.read()

    assert "rayon" in cargo_contents, "rayon crate is missing from Cargo.toml"

    # Search for parallel iteration in Rust source files
    src_dir = "/home/user/solver/src"
    assert os.path.exists(src_dir) and os.path.isdir(src_dir), f"Rust source directory not found at {src_dir}"

    found_par = False
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".rs"):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if "par_iter" in content or "into_par_iter" in content or "par_bridge" in content:
                        found_par = True
                        break
        if found_par:
            break

    assert found_par, "No parallel iteration (e.g., par_iter, into_par_iter) found in Rust source code"