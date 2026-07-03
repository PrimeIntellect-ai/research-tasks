# test_final_state.py
import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/evaluate_deployments.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not found."

def test_deployment_report_exists():
    report_path = "/home/user/deployment_report.json"
    assert os.path.isfile(report_path), f"The output file {report_path} was not found."

def test_deployment_report_content():
    report_path = "/home/user/deployment_report.json"
    assert os.path.isfile(report_path), f"The output file {report_path} was not found."

    with open(report_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected = {
        "core-update-v2": True,
        "ui-hotfix": True,
        "legacy-db-rollback": False,
        "complex-gateway": True
    }

    assert isinstance(results, dict), f"Expected a JSON object (dictionary), got {type(results).__name__}"

    for key, expected_val in expected.items():
        assert key in results, f"Manifest ID '{key}' is missing from the report."
        assert results[key] == expected_val, f"Expected manifest '{key}' to evaluate to {expected_val}, but got {results[key]}."

    # Check for extra keys
    extra_keys = set(results.keys()) - set(expected.keys())
    assert not extra_keys, f"Found unexpected manifest IDs in the report: {extra_keys}"