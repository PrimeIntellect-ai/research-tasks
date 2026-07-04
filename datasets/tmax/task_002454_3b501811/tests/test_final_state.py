# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/run_stability_test.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_summary_tsv_exists():
    summary_path = "/home/user/summary.tsv"
    assert os.path.isfile(summary_path), f"Summary file not found at {summary_path}"

def test_summary_tsv_content():
    summary_path = "/home/user/summary.tsv"
    if not os.path.isfile(summary_path):
        pytest.fail(f"Cannot test content, {summary_path} does not exist")

    with open(summary_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected 6 lines in summary.tsv (1 header + 5 data rows), found {len(lines)}"

    header = lines[0]
    expected_header = "NoiseLevel\tEstimatedMu"
    assert header == expected_header, f"Incorrect header. Expected '{expected_header}', got '{header}'"

    expected_noise_levels = ["0.1", "0.2", "0.3", "0.4", "0.5"]
    actual_noise_levels = []

    for i, line in enumerate(lines[1:], start=1):
        parts = line.split('\t')
        assert len(parts) == 2, f"Line {i+1} is not tab-separated properly: '{line}'"

        noise_level_str, mu_str = parts
        actual_noise_levels.append(noise_level_str)

        try:
            mu = float(mu_str)
        except ValueError:
            pytest.fail(f"EstimatedMu '{mu_str}' on line {i+1} is not a valid float")

        assert 14.0 <= mu <= 17.0, f"EstimatedMu {mu} on line {i+1} is too far from expected 15.5"

    # Check if noise levels are correct and sorted
    # Some students might write "0.1" or "0.10", so we parse as float for comparison
    actual_noise_floats = []
    for nl in actual_noise_levels:
        try:
            actual_noise_floats.append(float(nl))
        except ValueError:
            pytest.fail(f"NoiseLevel '{nl}' is not a valid float")

    expected_noise_floats = [0.1, 0.2, 0.3, 0.4, 0.5]
    assert actual_noise_floats == expected_noise_floats, f"Expected noise levels {expected_noise_floats}, got {actual_noise_floats}"

def test_output_files_exist():
    # Check if the generated data, notebooks, and json files exist for each noise level
    noise_levels = ["0.1", "0.2", "0.3", "0.4", "0.5"]
    for sigma in noise_levels:
        data_path = f"/home/user/data_noise_{sigma}.csv"
        nb_path = f"/home/user/mcmc_run_{sigma}.ipynb"
        json_path = f"/home/user/result_{sigma}.json"

        assert os.path.isfile(data_path), f"Missing generated dataset: {data_path}"
        assert os.path.isfile(nb_path), f"Missing executed notebook: {nb_path}"
        assert os.path.isfile(json_path), f"Missing result JSON: {json_path}"