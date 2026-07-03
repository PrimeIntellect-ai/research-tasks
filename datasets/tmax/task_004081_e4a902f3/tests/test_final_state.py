# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/compliance_audit_report.json"

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    assert os.path.isfile(REPORT_PATH), f"Path {REPORT_PATH} is not a file."

def test_report_format_and_content():
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON report: {e}")

    assert "total_violations" in data, "Key 'total_violations' missing from report."
    assert "high_risk_users" in data, "Key 'high_risk_users' missing from report."

    assert data["total_violations"] == 3, f"Expected 3 total violations, got {data['total_violations']}"

    high_risk_users = data["high_risk_users"]
    assert isinstance(high_risk_users, list), "'high_risk_users' should be a list."
    assert len(high_risk_users) == 2, f"Expected 2 high risk users, got {len(high_risk_users)}"

    # Check sorting of high_risk_users
    user_uris = [u.get("user_uri") for u in high_risk_users]
    assert user_uris == sorted(user_uris), "The 'high_risk_users' list must be sorted alphabetically by 'user_uri'."

    # Find Bob and Dave
    bob = next((u for u in high_risk_users if u.get("user_uri") == "http://example.org/ns#Bob"), None)
    dave = next((u for u in high_risk_users if u.get("user_uri") == "http://example.org/ns#Dave"), None)

    assert bob is not None, "User Bob is missing from high_risk_users."
    assert dave is not None, "User Dave is missing from high_risk_users."

    # Check violations for Bob
    bob_violations = bob.get("violations", [])
    assert isinstance(bob_violations, list), "Bob's 'violations' should be a list."
    assert bob_violations == sorted(bob_violations), "Bob's violations must be sorted alphabetically."
    assert bob_violations == ["LP_Dev_Write_Prod", "SoD_Dev_Auditor"], f"Bob's violations are incorrect: {bob_violations}"

    # Check violations for Dave
    dave_violations = dave.get("violations", [])
    assert isinstance(dave_violations, list), "Dave's 'violations' should be a list."
    assert dave_violations == sorted(dave_violations), "Dave's violations must be sorted alphabetically."
    assert dave_violations == ["LP_Dev_Write_Prod"], f"Dave's violations are incorrect: {dave_violations}"