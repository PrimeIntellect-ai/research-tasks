# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_valid():
    """Verify that results.json exists and has the correct structure."""
    file_path = "/home/user/results.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    assert "best_alpha" in results, "Key 'best_alpha' missing from results.json."
    assert "best_score" in results, "Key 'best_score' missing from results.json."

    assert isinstance(results["best_alpha"], (int, float)), "'best_alpha' must be a number."
    assert isinstance(results["best_score"], (int, float)), "'best_score' must be a number."

def test_results_json_values():
    """Verify the values in results.json match expected outputs."""
    file_path = "/home/user/results.json"
    if not os.path.isfile(file_path):
        pytest.skip("results.json not found")

    with open(file_path, 'r') as f:
        results = json.load(f)

    # best_alpha should be 10.0
    assert float(results["best_alpha"]) == 10.0, f"Expected best_alpha to be 10.0, got {results['best_alpha']}"

    # best_score should be approximately 0.9855
    score = float(results["best_score"])
    assert 0.98 < score < 0.99, f"Expected best_score to be around 0.9855, got {score}"

def test_processed_data_h5_exists_and_valid():
    """Verify that processed_data.h5 exists and is a valid HDF5 file."""
    file_path = "/home/user/processed_data.h5"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    # Check HDF5 magic number (\x89HDF\r\n\x1a\n)
    with open(file_path, 'rb') as f:
        magic = f.read(8)
        assert magic == b'\x89HDF\r\n\x1a\n', f"File {file_path} is not a valid HDF5 file (invalid signature)."

    # Check file size to ensure it's not empty (minimum size for HDF5 is usually > 800 bytes)
    assert os.path.getsize(file_path) > 1000, f"File {file_path} is too small to contain the dataset."