# test_final_state.py

import os
import json
import pytest

def test_incident_report_exists_and_correct():
    report_path = "/home/user/incident_report.json"
    assert os.path.isfile(report_path), f"Incident report not found at {report_path}"

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {report_path} is not valid JSON.")

    assert "cwe_vulnerabilities" in report_data, "Missing 'cwe_vulnerabilities' in report."
    assert "decrypted_log_secret" in report_data, "Missing 'decrypted_log_secret' in report."
    assert "backdoor_port" in report_data, "Missing 'backdoor_port' in report."

    expected_cwes = ["CWE-79", "CWE-89"]
    actual_cwes = report_data["cwe_vulnerabilities"]
    assert isinstance(actual_cwes, list), "'cwe_vulnerabilities' should be a list."
    assert sorted(actual_cwes) == expected_cwes, f"Expected CWEs {expected_cwes}, but got {actual_cwes}."

    expected_secret = "x89_FLAG_ZETA_992"
    actual_secret = report_data["decrypted_log_secret"]
    assert actual_secret == expected_secret, f"Expected secret '{expected_secret}', but got '{actual_secret}'."

    expected_port = 13042
    actual_port = report_data["backdoor_port"]
    assert actual_port == expected_port, f"Expected backdoor port {expected_port}, but got {actual_port}."