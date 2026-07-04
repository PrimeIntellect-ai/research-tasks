# test_final_state.py
import os
import json
import pytest

RESULTS_FILE = "/home/user/enforcement_results.json"

def test_results_file_exists():
    assert os.path.isfile(RESULTS_FILE), f"The expected output file {RESULTS_FILE} was not found."

def get_results():
    with open(RESULTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULTS_FILE} does not contain valid JSON.")

def test_project_alpha_results():
    results = get_results()
    assert "project_alpha" in results, "project_alpha is missing from the results."

    alpha = results["project_alpha"]
    assert alpha.get("status") == "pass", f"project_alpha status should be 'pass', got '{alpha.get('status')}'."

    reasons = alpha.get("reasons", [])
    assert isinstance(reasons, list), "project_alpha reasons should be a list."
    assert len(reasons) == 0, f"project_alpha reasons should be empty, got {reasons}."

def test_project_beta_results():
    results = get_results()
    assert "project_beta" in results, "project_beta is missing from the results."

    beta = results["project_beta"]
    assert beta.get("status") == "fail", f"project_beta status should be 'fail', got '{beta.get('status')}'."

    reasons = beta.get("reasons", [])
    assert isinstance(reasons, list), "project_beta reasons should be a list."
    expected_reasons = ["hardcoded_secrets_found", "invalid_token"]
    assert sorted(reasons) == expected_reasons, f"project_beta reasons should be {expected_reasons}, got {reasons}."

def test_project_gamma_results():
    results = get_results()
    assert "project_gamma" in results, "project_gamma is missing from the results."

    gamma = results["project_gamma"]
    assert gamma.get("status") == "fail", f"project_gamma status should be 'fail', got '{gamma.get('status')}'."

    reasons = gamma.get("reasons", [])
    assert isinstance(reasons, list), "project_gamma reasons should be a list."
    expected_reasons = ["privilege_escalation_risk"]
    assert sorted(reasons) == expected_reasons, f"project_gamma reasons should be {expected_reasons}, got {reasons}."