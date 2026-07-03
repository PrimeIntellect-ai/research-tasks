# test_final_state.py

import os
import json

def test_report_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"Report file {report_path} was not created."
    assert os.path.isfile(report_path), f"{report_path} is not a valid file."

    try:
        with open(report_path, 'r') as f:
            report_data = json.load(f)
    except json.JSONDecodeError as e:
        assert False, f"Failed to parse {report_path} as JSON: {e}"

    assert "exploits" in report_data, "The JSON report is missing the 'exploits' key."
    assert isinstance(report_data["exploits"], list), "The 'exploits' key must contain a list."

    expected_exploits = [
        {
            "ip": "172.16.0.44",
            "target_url": "http://evil-phishing.com/login"
        },
        {
            "ip": "203.0.113.88",
            "target_url": "https://steal-credentials.org/"
        }
    ]

    # Sort both lists by IP to ensure order doesn't cause a failure
    actual_exploits = sorted(report_data["exploits"], key=lambda x: x.get("ip", ""))
    expected_exploits_sorted = sorted(expected_exploits, key=lambda x: x["ip"])

    assert len(actual_exploits) == len(expected_exploits_sorted), \
        f"Expected {len(expected_exploits_sorted)} exploits, but found {len(actual_exploits)}."

    for actual, expected in zip(actual_exploits, expected_exploits_sorted):
        assert actual.get("ip") == expected["ip"], \
            f"Expected IP {expected['ip']}, but got {actual.get('ip')}."
        assert actual.get("target_url") == expected["target_url"], \
            f"Expected target_url {expected['target_url']}, but got {actual.get('target_url')}."