# test_final_state.py

import json
import os
import pytest

def test_output_json_metrics():
    output_path = "/home/user/output.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not a valid JSON file.")

    assert "frequency" in data, "Missing 'frequency' in output JSON."
    assert "integral" in data, "Missing 'integral' in output JSON."
    assert "frequency_std" in data, "Missing 'frequency_std' in output JSON."

    try:
        freq = float(data["frequency"])
        std = float(data["frequency_std"])
    except ValueError:
        pytest.fail("Values in JSON must be convertible to floats.")

    expected_freq = 2.5
    freq_error = abs(freq - expected_freq) / expected_freq

    assert freq_error <= 0.1, f"Frequency error {freq_error:.4f} exceeds threshold of 0.1. Extracted freq: {freq}, Expected: {expected_freq}"
    assert std > 0, f"Frequency standard deviation must be > 0, got {std}"

def test_script_exists():
    script_path = "/home/user/run_analysis.sh"
    assert os.path.exists(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."