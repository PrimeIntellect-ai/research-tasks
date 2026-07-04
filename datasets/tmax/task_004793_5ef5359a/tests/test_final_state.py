# test_final_state.py

import os
import json

def test_audit_report_exists():
    """Test that the audit_report.json file was created."""
    file_path = "/home/user/audit_report.json"
    assert os.path.exists(file_path), f"File {file_path} does not exist. The C++ program may not have run successfully or failed to write the output."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_audit_report_content():
    """Test that the audit_report.json contains the correct suspicious accounts and cycles."""
    file_path = "/home/user/audit_report.json"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse {file_path} as JSON: {e}"

    assert "suspicious_accounts" in data, "The JSON output is missing the 'suspicious_accounts' key."
    assert "cycles" in data, "The JSON output is missing the 'cycles' key."

    suspicious_accounts = data["suspicious_accounts"]
    cycles = data["cycles"]

    expected_suspicious_accounts = ["ACC123", "ACC456"]

    assert isinstance(suspicious_accounts, list), "'suspicious_accounts' must be a list."
    assert sorted(suspicious_accounts) == expected_suspicious_accounts, \
        f"Expected suspicious_accounts to be {expected_suspicious_accounts}, but got {suspicious_accounts}."

    expected_cycles = [
        ["ACC123", "ACC999", "ACC888"],
        ["ACC456", "ACC777", "ACC666"]
    ]

    assert isinstance(cycles, list), "'cycles' must be a list."

    # Sort both the expected and actual cycles to ensure order-independent comparison
    # The task specifies sorting the cycles lexicographically based on JSON string representation.
    # We will just check if the sorted lists of lists match.
    sorted_actual_cycles = sorted(cycles)
    sorted_expected_cycles = sorted(expected_cycles)

    assert sorted_actual_cycles == sorted_expected_cycles, \
        f"Expected cycles to be {sorted_expected_cycles}, but got {sorted_actual_cycles}."