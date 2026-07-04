# test_final_state.py
import os
import json
import re

def test_redacted_logs_exist_and_valid():
    redacted_path = "/home/user/investigation/http_logs_redacted.json"
    assert os.path.isfile(redacted_path), f"Redacted logs file missing: {redacted_path}"

    with open(redacted_path, "r") as f:
        try:
            redacted_logs = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{redacted_path} is not valid JSON"

    assert isinstance(redacted_logs, list), "Redacted HTTP logs should be a JSON list"

def test_redacted_logs_content():
    original_path = "/home/user/investigation/http_logs.json"
    redacted_path = "/home/user/investigation/http_logs_redacted.json"

    with open(original_path, "r") as f:
        original_logs = json.load(f)

    with open(redacted_path, "r") as f:
        redacted_logs = json.load(f)

    assert len(original_logs) == len(redacted_logs), "Redacted logs must have the same number of entries as the original."

    ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

    for orig, red in zip(original_logs, redacted_logs):
        # Check that top-level keys match
        assert set(orig.keys()) == set(red.keys()), "Redacted logs must have identical structure to original logs."

        # Check non-nested fields
        for key in ["timestamp", "source_ip", "method", "path"]:
            assert orig.get(key) == red.get(key), f"Field '{key}' was altered incorrectly."

        # Check headers
        orig_headers = orig.get("headers", {})
        red_headers = red.get("headers", {})
        assert set(orig_headers.keys()) == set(red_headers.keys()), "Headers keys must remain identical."

        for hk, hv in orig_headers.items():
            expected_val = ssn_pattern.sub("XXX-XX-XXXX", hv)
            assert red_headers[hk] == expected_val, f"Header '{hk}' was not redacted correctly."

        # Check cookies
        orig_cookies = orig.get("cookies", {})
        red_cookies = red.get("cookies", {})
        assert set(orig_cookies.keys()) == set(red_cookies.keys()), "Cookies keys must remain identical."

        for ck, cv in orig_cookies.items():
            expected_val = ssn_pattern.sub("XXX-XX-XXXX", cv)
            assert red_cookies[ck] == expected_val, f"Cookie '{ck}' was not redacted correctly."

def test_forensic_summary_exists_and_valid():
    summary_path = "/home/user/forensic_summary.json"
    assert os.path.isfile(summary_path), f"Forensic summary file missing: {summary_path}"

    with open(summary_path, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_path} is not valid JSON"

    assert isinstance(summary, dict), "Forensic summary should be a JSON object (dictionary)"

def test_forensic_summary_content():
    summary_path = "/home/user/forensic_summary.json"
    with open(summary_path, "r") as f:
        summary = json.load(f)

    expected_keys = {"privesc_vector", "malicious_ip", "exfiltrated_records_count"}
    assert set(summary.keys()) == expected_keys, f"Forensic summary must contain exactly these keys: {expected_keys}"

    assert summary["privesc_vector"] == "/home/user/investigation/system_dump/opt/maintenance/cleanup.sh", \
        "Incorrect privesc_vector in forensic summary."

    assert summary["malicious_ip"] == "203.0.113.88", \
        "Incorrect malicious_ip in forensic summary."

    assert summary["exfiltrated_records_count"] == 2, \
        "Incorrect exfiltrated_records_count in forensic summary."