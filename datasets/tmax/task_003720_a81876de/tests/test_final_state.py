# test_final_state.py

import os
import json
import pytest

def test_virtual_environment_exists():
    venv_python = "/home/user/perf_env/bin/python"
    assert os.path.exists(venv_python), f"Virtual environment python not found at {venv_python}"
    assert os.path.isfile(venv_python), f"{venv_python} is not a valid file"

def test_script_exists():
    script_path = "/home/user/analyze_perf.py"
    assert os.path.exists(script_path), f"Python script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a valid file"

def test_report_exists_and_valid():
    report_path = "/home/user/perf_report.json"
    assert os.path.exists(report_path), f"JSON report not found at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a valid file"

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON")

    assert "wasserstein_distance" in report_data, "Key 'wasserstein_distance' missing from report"
    assert "ks_p_value" in report_data, "Key 'ks_p_value' missing from report"

    w_dist = report_data["wasserstein_distance"]
    ks_p = report_data["ks_p_value"]

    assert isinstance(w_dist, (int, float)), "wasserstein_distance must be a number"
    assert isinstance(ks_p, (int, float)), "ks_p_value must be a number"

    expected_w_dist = 5.7538
    expected_ks_p = 0.0

    assert abs(w_dist - expected_w_dist) <= 0.0002, f"wasserstein_distance {w_dist} is not within acceptable range of {expected_w_dist}"
    assert abs(ks_p - expected_ks_p) <= 0.0001, f"ks_p_value {ks_p} is not within acceptable range of {expected_ks_p}"