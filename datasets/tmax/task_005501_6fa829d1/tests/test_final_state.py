# test_final_state.py

import os
import json
import math

def test_results_json_exists_and_valid():
    """Check that results.json exists and contains the correct structure and values."""
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"File {results_path} does not exist. The Go program may not have run or failed to output."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {results_path} is not valid JSON."

    expected_keys = {"k", "residual_mean", "residual_std"}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    # Check types
    assert isinstance(results["k"], int), f"Expected 'k' to be an integer, got {type(results['k']).__name__}"
    assert isinstance(results["residual_mean"], (int, float)), "Expected 'residual_mean' to be a float"
    assert isinstance(results["residual_std"], (int, float)), "Expected 'residual_std' to be a float"

    # The dataset was generated with a rank-3 base signal + noise.
    # Therefore, 95% variance is captured by exactly 3 components.
    assert results["k"] == 3, f"Expected k=3 based on the dataset's intrinsic rank, but got {results['k']}"

    # The residual mean should be extremely close to 0 since the data was centered.
    assert abs(results["residual_mean"]) < 1e-4, f"Expected residual_mean close to 0, got {results['residual_mean']}"

    # The noise added during setup had a standard deviation of 0.5.
    # The residual standard deviation should closely match this.
    assert 0.45 < results["residual_std"] < 0.55, f"Expected residual_std to be around 0.5, got {results['residual_std']}"

def test_go_source_exists():
    """Verify that the Go source file was created."""
    source_path = '/home/user/process.go'
    assert os.path.exists(source_path), f"Go source file {source_path} does not exist."
    assert os.path.isfile(source_path), f"Path {source_path} is not a file."

def test_go_module_initialized():
    """Verify that a Go module was initialized."""
    mod_path = '/home/user/go.mod'
    assert os.path.exists(mod_path), "Go module was not initialized. Missing /home/user/go.mod"