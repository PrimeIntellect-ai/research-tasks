# test_final_state.py

import os
import json
import pytest

def test_spectral_analysis_output():
    output_path = "/home/user/spectral_analysis.json"
    expected_path = "/tmp/expected_output.json"

    assert os.path.isfile(output_path), f"Output file is missing: {output_path}"
    assert os.path.isfile(expected_path), f"Expected output file is missing: {expected_path}"

    with open(output_path, 'r') as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON.")

    with open(expected_path, 'r') as f:
        expected_data = json.load(f)

    expected_keys = {"max_psd_index", "max_psd_value", "mc_threshold_95"}
    assert set(output_data.keys()) == expected_keys, f"Output JSON keys do not match expected keys. Found: {list(output_data.keys())}"

    assert isinstance(output_data["max_psd_index"], int), "max_psd_index must be an integer"
    assert isinstance(output_data["max_psd_value"], float), "max_psd_value must be a float"
    assert isinstance(output_data["mc_threshold_95"], float), "mc_threshold_95 must be a float"

    assert output_data["max_psd_index"] == expected_data["max_psd_index"], f"max_psd_index mismatch: expected {expected_data['max_psd_index']}, got {output_data['max_psd_index']}"
    assert output_data["max_psd_value"] == expected_data["max_psd_value"], f"max_psd_value mismatch: expected {expected_data['max_psd_value']}, got {output_data['max_psd_value']}"
    assert output_data["mc_threshold_95"] == expected_data["mc_threshold_95"], f"mc_threshold_95 mismatch: expected {expected_data['mc_threshold_95']}, got {output_data['mc_threshold_95']}"