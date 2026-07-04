# test_final_state.py

import os
import json
import subprocess
import pytest

def test_executable_exists():
    """Check that the compiled Go executable exists."""
    exe_path = "/home/user/bin/mahalanobis_calc"
    assert os.path.isfile(exe_path), f"Executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_results_json_exists_and_format():
    """Check that results.json exists and has the correct format."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    expected_keys = {"ci_lower", "ci_upper", "p_value"}
    assert set(data.keys()) == expected_keys, f"results.json must contain exactly keys: {expected_keys}"

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Value for {key} must be a number"

def test_go_code_modified_for_ridge():
    """Check that the Go source code was modified to add 0.0001 to the diagonal."""
    main_go_path = "/home/user/src/mahalanobis/main.go"
    assert os.path.isfile(main_go_path), f"Source file not found at {main_go_path}"

    with open(main_go_path, "r") as f:
        content = f.read()

    # Check for evidence of ridge regularization
    assert "0.0001" in content, "Could not find the Ridge regularization constant (0.0001) in main.go"

def test_bootstrap_logic_in_source():
    """Check that bootstrap and seed logic is present in the source directory."""
    src_dir = "/home/user/src/mahalanobis"
    found_seed = False
    found_bootstrap = False

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".go") or file.endswith(".sh") or file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "42" in content and ("Seed" in content or "seed" in content):
                        found_seed = True
                    if "10000" in content or "10,000" in content:
                        found_bootstrap = True

    assert found_seed, "Could not find seed initialization (e.g., Seed(42)) in the source files."
    assert found_bootstrap, "Could not find 10000 iterations for bootstrap in the source files."