# test_final_state.py

import os
import json
import pytest

def test_clean_audit_exists():
    path = "/home/user/clean_audit.json"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_clean_audit_content():
    path = "/home/user/clean_audit.json"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert isinstance(logs, list), "The JSON root should be a list of dictionaries."
    assert len(logs) == 4, f"Expected 4 logs, found {len(logs)}."

    # Check redactions
    assert logs[1].get("message") == "Payment processed for card [REDACTED] successfully.", \
        "Credit card number in format XXXX-XXXX-XXXX-XXXX was not redacted correctly."

    assert logs[3].get("message") == "Direct billing account updated for [REDACTED].", \
        "Credit card number in format XXXXXXXXXXXXXXXX was not redacted correctly."

    # Check cert_issuer enrichment
    for i, log in enumerate(logs):
        assert "cert_issuer" in log, f"Log at index {i} is missing 'cert_issuer' key."
        assert log["cert_issuer"] == "ComplianceCA", \
            f"Log at index {i} has incorrect 'cert_issuer': {log['cert_issuer']}."

def test_clean_audit_formatting():
    path = "/home/user/clean_audit.json"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for 2-space indentation
    # A simple heuristic is to check if there are lines starting with exactly two spaces followed by a quote
    lines = content.split('\n')
    has_two_space_indent = any(line.startswith("  \"") for line in lines)
    assert has_two_space_indent, "The JSON file does not appear to be pretty-printed with a 2-space indent."