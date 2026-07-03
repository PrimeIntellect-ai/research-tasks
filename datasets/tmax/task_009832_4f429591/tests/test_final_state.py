# test_final_state.py

import os
import json
import math
import pytest

def test_executable_exists():
    """Check that the C++ solver was compiled to the correct location."""
    exe_path = "/home/user/bin/solver"
    assert os.path.isfile(exe_path), f"Executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_raw_peaks_csv_exists():
    """Check that the raw_peaks.csv file was generated."""
    csv_path = "/home/user/data/raw_peaks.csv"
    assert os.path.isfile(csv_path), f"Data file not found at {csv_path}"

    with open(csv_path, "r") as f:
        lines = f.readlines()
    assert len(lines) > 1, f"{csv_path} does not contain enough data"
    assert "intensity,frequency" in lines[0], f"Header missing or incorrect in {csv_path}"

def test_process_spectra_script_exists():
    """Check that the Python processing script exists."""
    script_path = "/home/user/process_spectra.py"
    assert os.path.isfile(script_path), f"Python script not found at {script_path}"

def test_summary_json():
    """Check the final JSON output for correct keys and values."""
    json_path = "/home/user/data/summary.json"
    assert os.path.isfile(json_path), f"JSON summary not found at {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file")

    assert "convergence_max_iterations" in data, "Key 'convergence_max_iterations' missing from JSON"
    assert "wasserstein_distance" in data, "Key 'wasserstein_distance' missing from JSON"

    # Check convergence iterations
    # The C++ code runs 10 iterations, max_iter should be 4
    assert data["convergence_max_iterations"] == 4, \
        f"Expected convergence_max_iterations to be 4, got {data['convergence_max_iterations']}"

    # Check Wasserstein distance
    # The expected value is approx 0.287213 based on np.random.seed(42)
    expected_w_dist = 0.287213
    actual_w_dist = data["wasserstein_distance"]

    assert isinstance(actual_w_dist, (int, float)), "wasserstein_distance must be a number"
    assert math.isclose(actual_w_dist, expected_w_dist, abs_tol=1e-5), \
        f"Expected wasserstein_distance to be near {expected_w_dist}, got {actual_w_dist}"