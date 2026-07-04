# test_final_state.py

import os
import json
import pytest

def test_experiment_directory_exists():
    """Test that the experiment directory exists."""
    assert os.path.isdir("/home/user/experiment"), "Directory /home/user/experiment does not exist."

def test_metadata_json():
    """Test that metadata.json exists and contains the correct values."""
    metadata_path = "/home/user/experiment/metadata.json"
    assert os.path.isfile(metadata_path), f"File {metadata_path} does not exist."

    with open(metadata_path, "r") as f:
        try:
            metadata = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metadata_path} is not valid JSON.")

    assert isinstance(metadata, dict), "metadata.json must contain a JSON object."
    assert "n_samples" in metadata, "Key 'n_samples' missing in metadata.json"
    assert "n_features" in metadata, "Key 'n_features' missing in metadata.json"
    assert metadata["n_samples"] == 7, f"Expected n_samples=7, got {metadata['n_samples']}"
    assert metadata["n_features"] == 4, f"Expected n_features=4, got {metadata['n_features']}"

def test_weights_json():
    """Test that weights.json exists and contains the correct MAP estimates."""
    weights_path = "/home/user/experiment/weights.json"
    assert os.path.isfile(weights_path), f"File {weights_path} does not exist."

    with open(weights_path, "r") as f:
        try:
            weights = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {weights_path} is not valid JSON.")

    assert isinstance(weights, list), "weights.json must contain a JSON array."
    assert len(weights) == 4, f"Expected 4 elements in weights array, got {len(weights)}."

    # Pre-computed expected weights from the exact formula
    expected_weights = [
        0.03813959954067339,
        0.05030239617260029,
        0.046036128859942735,
        0.17056463991823942
    ]

    for i, (w, expected_w) in enumerate(zip(weights, expected_weights)):
        assert isinstance(w, (int, float)), f"Weight at index {i} is not a number."
        assert abs(w - expected_w) < 1e-4, f"Weight at index {i} is {w}, expected approximately {expected_w}."