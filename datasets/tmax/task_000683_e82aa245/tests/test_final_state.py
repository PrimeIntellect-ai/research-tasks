# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Expected report file at {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    # Check Alpha dictionary
    assert "Alpha" in report_data, "Missing 'Alpha' key in report.json"
    alpha = report_data["Alpha"]
    assert alpha.get("clicks") == 1000, f"Expected Alpha clicks to be 1000, got {alpha.get('clicks')}"
    assert alpha.get("conversions") == 95, f"Expected Alpha conversions to be 95, got {alpha.get('conversions')}"
    assert abs(alpha.get("posterior_mean", 0) - 0.09581) <= 0.00002, f"Expected Alpha posterior_mean to be approx 0.09581, got {alpha.get('posterior_mean')}"

    # Check Beta dictionary
    assert "Beta" in report_data, "Missing 'Beta' key in report.json"
    beta = report_data["Beta"]
    assert beta.get("clicks") == 1200, f"Expected Beta clicks to be 1200, got {beta.get('clicks')}"
    assert beta.get("conversions") == 130, f"Expected Beta conversions to be 130, got {beta.get('conversions')}"
    assert abs(beta.get("posterior_mean", 0) - 0.10908) <= 0.00002, f"Expected Beta posterior_mean to be approx 0.10908, got {beta.get('posterior_mean')}"

    # Check probability
    assert "prob_alpha_greater_beta" in report_data, "Missing 'prob_alpha_greater_beta' key in report.json"
    prob = report_data["prob_alpha_greater_beta"]
    assert abs(prob - 0.13404) <= 0.00002, f"Expected prob_alpha_greater_beta to be approx 0.13404, got {prob}"