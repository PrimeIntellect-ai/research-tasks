# test_final_state.py

import os
import json
import base64
import urllib.parse
import pytest

def fully_url_decode(val: str) -> str:
    decoded = urllib.parse.unquote(val)
    while True:
        new_decoded = urllib.parse.unquote(decoded)
        if new_decoded == decoded:
            break
        decoded = new_decoded
    return decoded

def compute_expected_findings(logs_path: str) -> list:
    with open(logs_path, "r") as f:
        logs = json.load(f)

    findings = []
    for entry in logs:
        flags = []
        url = entry.get("url", "")
        headers = entry.get("headers", {})

        # Parse redirect parameter
        parsed_url = urllib.parse.urlparse(url)
        redirect_val = None
        for param in parsed_url.query.split("&"):
            if param.startswith("redirect="):
                redirect_val = param.split("=", 1)[1]
                break

        if redirect_val is not None:
            decoded = fully_url_decode(redirect_val)

            # Check open_redirect
            if decoded.startswith("http://") or decoded.startswith("https://"):
                if not (decoded.startswith("http://example.com") or decoded.startswith("https://example.com")):
                    flags.append("open_redirect")

            # Check xss
            lower_decoded = decoded.lower()
            if "<script" in lower_decoded or "javascript:" in lower_decoded:
                flags.append("xss")

        # Check privesc
        auth = headers.get("Authorization", "")
        if auth.startswith("Basic "):
            b64_payload = auth[6:]
            try:
                decoded_auth = base64.b64decode(b64_payload).decode("utf-8")
                if "role=admin" in decoded_auth:
                    flags.append("privesc")
            except Exception:
                pass

        if flags:
            findings.append({
                "id": entry.get("id"),
                "flags": sorted(flags)
            })

    # Sort the outer array alphabetically by 'id'
    findings.sort(key=lambda x: x["id"])
    return findings

def test_findings_json_exists_and_correct():
    logs_path = "/home/user/logs.json"
    findings_path = "/home/user/findings.json"

    assert os.path.exists(logs_path), f"The file {logs_path} is missing, cannot compute expected findings."
    assert os.path.exists(findings_path), f"The file {findings_path} is missing. Did the tool run successfully?"
    assert os.path.isfile(findings_path), f"The path {findings_path} is not a file."

    with open(findings_path, "r") as f:
        try:
            actual_findings = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {findings_path} does not contain valid JSON.")

    expected_findings = compute_expected_findings(logs_path)

    assert isinstance(actual_findings, list), f"The content of {findings_path} must be a JSON array."
    assert len(actual_findings) == len(expected_findings), f"Expected {len(expected_findings)} findings, but got {len(actual_findings)}."

    for i, (actual, expected) in enumerate(zip(actual_findings, expected_findings)):
        assert actual.get("id") == expected["id"], f"Finding at index {i} has incorrect 'id'. Expected '{expected['id']}', got '{actual.get('id')}'."

        actual_flags = actual.get("flags", [])
        expected_flags = expected["flags"]

        assert isinstance(actual_flags, list), f"The 'flags' field for id '{actual['id']}' must be an array."
        assert actual_flags == expected_flags, f"Flags for id '{actual['id']}' are incorrect. Expected {expected_flags}, got {actual_flags}."