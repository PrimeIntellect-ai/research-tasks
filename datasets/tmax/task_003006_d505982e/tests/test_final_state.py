# test_final_state.py

import os
import json
import subprocess
import pytest

def test_venv_and_packages():
    """Test that the virtual environment is created and required packages are installed."""
    python_path = '/home/user/ml_env/bin/python'
    assert os.path.isfile(python_path), f"Virtual environment python not found at {python_path}. Did you create the venv?"

    # Check installed packages
    result = subprocess.run([python_path, '-m', 'pip', 'freeze'], capture_output=True, text=True)
    installed_packages = result.stdout.lower()

    assert 'numpy' in installed_packages, "numpy is not installed in the virtual environment."
    assert 'pandas' in installed_packages, "pandas is not installed in the virtual environment."
    assert 'scipy' in installed_packages, "scipy is not installed in the virtual environment."

def test_training_features_output():
    """Test that the output JSON file exists, has the correct structure, and contains expected values."""
    file_path = '/home/user/training_features.json'
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    # Check structure
    assert "dominant_frequencies" in data, "Missing 'dominant_frequencies' in output JSON."
    assert "is_valid_analytical" in data, "Missing 'is_valid_analytical' in output JSON."
    assert "baseline_differences" in data, "Missing 'baseline_differences' in output JSON."

    # Check analytical flag
    assert data["is_valid_analytical"] is True, "'is_valid_analytical' should be true based on the calculated dominant frequency of seg_1."

    # Check dominant frequencies
    expected_freqs = {
        "seg_0": 5.0,
        "seg_1": 12.5,
        "seg_2": 20.0,
        "seg_3": 35.0
    }
    for k, v in expected_freqs.items():
        assert k in data["dominant_frequencies"], f"Missing {k} in dominant_frequencies."
        actual_freq = data["dominant_frequencies"][k]
        assert isinstance(actual_freq, (int, float)), f"Dominant frequency for {k} must be a number."
        assert abs(actual_freq - v) < 0.05, f"Incorrect dominant frequency for {k}. Expected {v}, got {actual_freq}."

    # Check baseline differences
    expected_diffs = {
        "seg_0": 0.0,
        "seg_1": 0.5,
        "seg_2": 0.5,
        "seg_3": 1.0
    }
    for k, v in expected_diffs.items():
        assert k in data["baseline_differences"], f"Missing {k} in baseline_differences."
        actual_diff = data["baseline_differences"][k]
        assert isinstance(actual_diff, (int, float)), f"Baseline difference for {k} must be a number."
        assert abs(actual_diff - v) < 0.05, f"Incorrect baseline difference for {k}. Expected {v}, got {actual_diff}."