# test_final_state.py
import os
import json
import pytest

def test_pca_plot_created():
    """Verify that the PCA plot image was created and is not empty."""
    plot_path = '/home/user/pca_plot.png'
    assert os.path.isfile(plot_path), f"Expected plot file at {plot_path} is missing."
    assert os.path.getsize(plot_path) > 0, f"Plot file at {plot_path} is empty."

def test_tracking_json_created_and_valid():
    """Verify that the tracking JSON file exists and contains the correct structure and invariants."""
    json_path = '/home/user/tracking.json'
    assert os.path.isfile(json_path), f"Expected tracking JSON file at {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {json_path} is not valid JSON.")

    assert "n_components" in result, "Key 'n_components' is missing from tracking.json."
    assert "variance_explained" in result, "Key 'variance_explained' is missing from tracking.json."

    n_comp = result["n_components"]
    var_expl = result["variance_explained"]

    assert isinstance(n_comp, int), f"'n_components' should be an integer, got {type(n_comp).__name__}."
    assert isinstance(var_expl, float), f"'variance_explained' should be a float, got {type(var_expl).__name__}."

    assert n_comp > 0, f"'n_components' must be strictly positive, got {n_comp}."
    assert var_expl >= 0.85, f"'variance_explained' must be >= 0.85, got {var_expl}."
    assert var_expl <= 1.0, f"'variance_explained' must be <= 1.0, got {var_expl}."