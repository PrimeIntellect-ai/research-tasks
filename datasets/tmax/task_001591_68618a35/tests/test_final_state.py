# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists_and_valid():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist. Ensure your script generated it."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_keys = {"attacker_ip", "cracked_password", "privesc_command"}
    missing_keys = expected_keys - set(report_data.keys())
    assert not missing_keys, f"The JSON report is missing the following required keys: {missing_keys}"

    assert report_data["attacker_ip"] == "10.0.0.55", \
        f"Expected attacker_ip to be '10.0.0.55', but got '{report_data['attacker_ip']}'."

    assert report_data["cracked_password"] == "compliance2023", \
        f"Expected cracked_password to be 'compliance2023', but got '{report_data['cracked_password']}'."

    assert report_data["privesc_command"] == "/usr/bin/tar", \
        f"Expected privesc_command to be '/usr/bin/tar', but got '{report_data['privesc_command']}'."