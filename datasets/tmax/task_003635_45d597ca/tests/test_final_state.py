# test_final_state.py

import os
import json
import pytest

def test_pca_stability_json_exists():
    """Test that the output JSON file exists."""
    file_path = '/home/user/pca_stability.json'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

def test_pca_stability_json_structure_and_values():
    """Test the structure and invariants of the PCA stability JSON."""
    file_path = '/home/user/pca_stability.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {"mean_pc1_var", "ci_lower", "ci_upper"}
    assert set(result.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, got {set(result.keys())}"

    mean_var = result["mean_pc1_var"]
    ci_lower = result["ci_lower"]
    ci_upper = result["ci_upper"]

    assert isinstance(mean_var, float), "mean_pc1_var must be a float"
    assert isinstance(ci_lower, float), "ci_lower must be a float"
    assert isinstance(ci_upper, float), "ci_upper must be a float"

    # Variance explained must be between 0 and 1
    assert 0.0 <= mean_var <= 1.0, f"mean_pc1_var {mean_var} is out of bounds [0, 1]"
    assert 0.0 <= ci_lower <= 1.0, f"ci_lower {ci_lower} is out of bounds [0, 1]"
    assert 0.0 <= ci_upper <= 1.0, f"ci_upper {ci_upper} is out of bounds [0, 1]"

    # Check logical relationships
    assert ci_lower <= mean_var, f"ci_lower ({ci_lower}) should be <= mean_pc1_var ({mean_var})"
    assert mean_var <= ci_upper, f"mean_pc1_var ({mean_var}) should be <= ci_upper ({ci_upper})"