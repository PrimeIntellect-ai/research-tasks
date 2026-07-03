# test_final_state.py

import json
import os
import pytest

def test_report_exists():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

def test_report_content_and_logic():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Cannot test content because {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "reference" in data, "The JSON report is missing the 'reference' key."
    assert "simulation" in data, "The JSON report is missing the 'simulation' key."

    ref = data["reference"]
    sim = data["simulation"]

    expected_keys = ["mean_peak_freq", "ci_lower", "ci_upper"]
    for key in expected_keys:
        assert key in ref, f"The 'reference' object is missing the '{key}' key."
        assert key in sim, f"The 'simulation' object is missing the '{key}' key."

        # Ensure they are numbers
        assert isinstance(ref[key], (int, float)), f"reference.{key} must be a number."
        assert isinstance(sim[key], (int, float)), f"simulation.{key} must be a number."

    ref_mean = ref["mean_peak_freq"]
    sim_mean = sim["mean_peak_freq"]

    assert 48.0 < ref_mean < 52.0, f"Reference mean_peak_freq ({ref_mean}) is out of expected bounds (48.0 - 52.0)."
    assert 75.0 < sim_mean < 85.0, f"Simulation mean_peak_freq ({sim_mean}) is out of expected bounds (75.0 - 85.0)."

    assert ref["ci_lower"] < ref_mean < ref["ci_upper"], \
        f"Reference confidence interval is invalid: {ref['ci_lower']} < {ref_mean} < {ref['ci_upper']} is False."

    assert sim["ci_lower"] < sim_mean < sim["ci_upper"], \
        f"Simulation confidence interval is invalid: {sim['ci_lower']} < {sim_mean} < {sim['ci_upper']} is False."