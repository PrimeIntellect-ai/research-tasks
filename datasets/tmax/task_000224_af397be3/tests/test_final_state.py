# test_final_state.py

import os
import json
import pytest

def test_compiled_binary_exists():
    binary_path = "/home/user/spectro_sim"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_generated_data_files():
    sim_data_dir = "/home/user/sim_data"
    assert os.path.exists(sim_data_dir), f"Directory {sim_data_dir} does not exist."

    for i in range(100):
        file_path = os.path.join(sim_data_dir, f"run_{i}.txt")
        assert os.path.exists(file_path), f"Data file {file_path} is missing."
        assert os.path.isfile(file_path), f"{file_path} is not a file."

        with open(file_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == 1000, f"{file_path} does not contain exactly 1000 lines."

        # Check if they are valid floats
        try:
            float(lines[0].strip())
            float(lines[-1].strip())
        except ValueError:
            pytest.fail(f"Contents of {file_path} are not valid floating-point numbers.")

def test_analyze_script_exists():
    script_path = "/home/user/analyze.py"
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {report_path} as JSON: {e}")

    required_keys = {
        "mean_peak": float,
        "variance_peak": float,
        "shapiro_statistic": float,
        "shapiro_p_value": float,
        "is_reproducible": bool
    }

    for key, expected_type in required_keys.items():
        assert key in data, f"Missing key '{key}' in {report_path}."
        assert isinstance(data[key], expected_type) or (expected_type == float and isinstance(data[key], int)), \
            f"Key '{key}' in {report_path} is not of expected type {expected_type.__name__}."

    assert data["is_reproducible"] is False, "is_reproducible should be false due to non-deterministic floating-point errors."
    assert data["variance_peak"] > 0.0, "variance_peak should be greater than 0.0."
    assert 400 < data["mean_peak"] < 600, f"mean_peak {data['mean_peak']} is out of expected bounds (400, 600)."