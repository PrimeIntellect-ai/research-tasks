# test_final_state.py
import os
import json
import pytest

def test_analysis_json_exists_and_correct():
    file_path = '/home/user/analysis.json'

    assert os.path.exists(file_path), f"The output file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    assert "dominant_freq_hz" in data, "The JSON is missing the 'dominant_freq_hz' key."
    assert "drift_slope" in data, "The JSON is missing the 'drift_slope' key."

    dominant_freq = data["dominant_freq_hz"]
    drift_slope = data["drift_slope"]

    assert isinstance(dominant_freq, int), f"Expected 'dominant_freq_hz' to be an integer, got {type(dominant_freq).__name__}."
    assert isinstance(drift_slope, (int, float)), f"Expected 'drift_slope' to be a float, got {type(drift_slope).__name__}."

    assert dominant_freq == 60, f"Expected dominant frequency to be 60 Hz, got {dominant_freq}."

    expected_slope = 0.0125
    assert abs(drift_slope - expected_slope) < 0.0002, f"Expected drift slope to be approximately {expected_slope}, got {drift_slope}."