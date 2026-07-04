# test_final_state.py
import os
import json
import pytest

def test_rust_project_exists():
    """Verify that the Rust project directory and basic files exist."""
    project_dir = "/home/user/signal_analysis"
    assert os.path.exists(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isdir(project_dir), f"{project_dir} is not a directory."

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.exists(cargo_toml), f"Cargo.toml not found at {cargo_toml}."

    main_rs = os.path.join(project_dir, "src", "main.rs")
    assert os.path.exists(main_rs), f"main.rs not found at {main_rs}."

def test_analysis_output_exists_and_valid_json():
    """Verify that the analysis_output.json file exists and is valid JSON."""
    output_file = "/home/user/analysis_output.json"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    assert isinstance(data, dict), "JSON root must be an object (dictionary)."

def test_analysis_output_structure_and_values():
    """Verify the contents of the analysis_output.json file."""
    output_file = "/home/user/analysis_output.json"
    if not os.path.exists(output_file):
        pytest.skip("Output file missing, skipping content validation.")

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Output file is invalid JSON, skipping content validation.")

    # Check matrix dimensions
    assert "matrix_dimensions" in data, "Missing 'matrix_dimensions' key."
    assert data["matrix_dimensions"] == [100, 20], f"Expected matrix_dimensions to be [100, 20], got {data['matrix_dimensions']}."

    # Check top_3_svd
    assert "top_3_svd" in data, "Missing 'top_3_svd' key."
    top_3_svd = data["top_3_svd"]
    assert isinstance(top_3_svd, list), "'top_3_svd' should be a list."
    assert len(top_3_svd) == 3, f"Expected 3 items in 'top_3_svd', got {len(top_3_svd)}."

    for i, sv_obj in enumerate(top_3_svd):
        assert isinstance(sv_obj, dict), f"Item {i} in 'top_3_svd' is not an object."
        for key in ["value", "ci_lower", "ci_upper"]:
            assert key in sv_obj, f"Missing '{key}' in 'top_3_svd' item {i}."
            assert isinstance(sv_obj[key], (int, float)), f"'{key}' in 'top_3_svd' item {i} must be a number."

        # Basic sanity check on CI
        assert sv_obj["ci_lower"] <= sv_obj["ci_upper"], f"ci_lower > ci_upper for item {i}."

    # Check SV1 range based on verification script
    sv1 = top_3_svd[0]["value"]
    assert 200.0 < sv1 < 300.0, f"SV1 value {sv1} is out of the expected range (200.0 - 300.0)."

    # Check distribution_l2_distance
    assert "distribution_l2_distance" in data, "Missing 'distribution_l2_distance' key."
    dist = data["distribution_l2_distance"]
    assert isinstance(dist, (int, float)), "'distribution_l2_distance' must be a number."
    assert 0.0 <= dist <= 1.0, f"'distribution_l2_distance' {dist} is out of range [0.0, 1.0]."