# test_final_state.py

import os
import json
import pytest

def test_plot_exists():
    """Verify that the generated plot exists."""
    plot_path = "/home/user/spectroscopy_analysis.png"
    assert os.path.exists(plot_path), f"Plot file {plot_path} does not exist."
    assert os.path.isfile(plot_path), f"{plot_path} is not a file."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."

def test_json_results():
    """Verify that the JSON results file exists and contains the correct data."""
    json_path = "/home/user/spectral_results.json"
    assert os.path.exists(json_path), f"JSON file {json_path} does not exist."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "detected_frequencies" in data, "Key 'detected_frequencies' missing in JSON."
    assert "max_amplitude_frequency" in data, "Key 'max_amplitude_frequency' missing in JSON."

    detected = data["detected_frequencies"]
    assert isinstance(detected, list), "'detected_frequencies' must be a list."
    assert len(detected) == 3, f"Expected 3 detected frequencies, got {len(detected)}."

    # Sort just in case, though the prompt requires them to be sorted.
    detected_sorted = sorted(detected)
    expected_frequencies = [50.0, 120.0, 200.0]

    for expected, actual in zip(expected_frequencies, detected_sorted):
        assert abs(expected - actual) < 1.0, f"Expected detected frequency near {expected}, got {actual}."

    max_freq = data["max_amplitude_frequency"]
    assert abs(120.0 - max_freq) < 1.0, f"Expected max amplitude frequency near 120.0, got {max_freq}."

def test_script_exists():
    """Verify that the Python script was created."""
    script_path = "/home/user/process_signal.py"
    assert os.path.exists(script_path), f"Script file {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."