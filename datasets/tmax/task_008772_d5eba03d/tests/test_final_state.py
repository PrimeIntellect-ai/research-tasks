# test_final_state.py

import os
import json

def test_results_json_exists():
    """Test that results.json exists and is a file."""
    file_path = "/home/user/results.json"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_results_json_content():
    """Test that results.json contains the correct scientific computing results."""
    file_path = "/home/user/results.json"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} does not contain valid JSON."

    required_keys = [
        "noise_sigma",
        "original_max_flux",
        "original_max_wavelength",
        "mc_mean_peak",
        "mc_std_peak",
        "p_value"
    ]

    for key in required_keys:
        assert key in data, f"Missing required key '{key}' in results.json."

    # Validate original spectrum max values
    assert abs(data['original_max_flux'] - 14.20) < 0.01, \
        f"Expected original_max_flux around 14.20, got {data['original_max_flux']}"
    assert abs(data['original_max_wavelength'] - 426.0) < 0.01, \
        f"Expected original_max_wavelength around 426.0, got {data['original_max_wavelength']}"

    # Validate noise estimation (allow either population or sample stddev)
    assert 0.07 < data['noise_sigma'] < 0.09, \
        f"Expected noise_sigma between 0.07 and 0.09, got {data['noise_sigma']}"

    # Validate Monte Carlo simulation results
    assert 14.1 < data['mc_mean_peak'] < 14.3, \
        f"Expected mc_mean_peak between 14.1 and 14.3, got {data['mc_mean_peak']}"
    assert 0.07 < data['mc_std_peak'] < 0.09, \
        f"Expected mc_std_peak between 0.07 and 0.09, got {data['mc_std_peak']}"

    # Validate statistical test p-value
    assert data['p_value'] < 1e-5, \
        f"Expected p_value < 1e-5, got {data['p_value']}"