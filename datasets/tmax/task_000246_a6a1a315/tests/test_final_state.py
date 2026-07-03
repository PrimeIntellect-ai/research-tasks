# test_final_state.py

import os
import json
import urllib.parse
import re
import pytest

def get_binary_strings(filepath):
    """Extracts the configuration strings from the binary."""
    with open(filepath, "rb") as f:
        content = f.read()

    trusted_domain_match = re.search(b"TRUSTED_DOMAIN=([a-zA-Z0-9.-]+)", content)
    secret_cookie_match = re.search(b"SECRET_COOKIE_NAME=([a-zA-Z0-9_.-]+)", content)

    trusted_domain = trusted_domain_match.group(1).decode('utf-8') if trusted_domain_match else "secure.internal.corp"
    secret_cookie = secret_cookie_match.group(1).decode('utf-8') if secret_cookie_match else "Admin_X_Session_Token"

    return trusted_domain, secret_cookie

def test_processed_traffic_exists():
    processed_path = "/home/user/processed_traffic.jsonl"
    assert os.path.exists(processed_path), f"Output file {processed_path} does not exist. Did you run your Go program?"
    assert os.path.isfile(processed_path), f"{processed_path} is not a file."

def test_processed_traffic_content():
    processed_path = "/home/user/processed_traffic.jsonl"
    binary_path = "/home/user/server_bin"

    trusted_domain, secret_cookie = get_binary_strings(binary_path)
    expected_csp = f"default-src 'self'; frame-ancestors 'none'; connect-src https://{trusted_domain}"

    with open(processed_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, f"File {processed_path} is empty."

    records = {}
    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            req_id = data.get("request_id")
            if req_id:
                records[req_id] = data
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {processed_path} is not valid JSON.")

    assert "req-001" in records, "req-001 is missing from the processed output."
    assert "req-002" in records, "req-002 is missing from the processed output."
    assert "req-003" in records, "req-003 is missing from the processed output."

    # Check req-001
    req1 = records["req-001"]
    assert req1.get("open_redirect_attempt") is False, "req-001 should have open_redirect_attempt as false."
    cookie1 = req1.get("headers", {}).get("Cookie", "")
    assert f"{secret_cookie}=[REDACTED]" in cookie1, f"req-001 Cookie does not have {secret_cookie} redacted."
    assert "user_pref=dark" in cookie1, "req-001 Cookie is missing other unmodified cookies."
    assert req1.get("injected_csp") == expected_csp, f"req-001 injected_csp is incorrect. Expected: {expected_csp}"

    # Check req-002
    req2 = records["req-002"]
    assert req2.get("open_redirect_attempt") is True, "req-002 should have open_redirect_attempt as true (evil-phishing.com)."
    cookie2 = req2.get("headers", {}).get("Cookie", "")
    assert "session=normaluser" in cookie2, "req-002 Cookie should remain unmodified."
    assert req2.get("injected_csp") == expected_csp, f"req-002 injected_csp is incorrect. Expected: {expected_csp}"

    # Check req-003
    req3 = records["req-003"]
    assert req3.get("open_redirect_attempt") is False, "req-003 should have open_redirect_attempt as false (no redirect)."
    cookie3 = req3.get("headers", {}).get("Cookie", "")
    assert cookie3 == f"{secret_cookie}=[REDACTED]", f"req-003 Cookie should be exactly {secret_cookie}=[REDACTED]."
    assert req3.get("injected_csp") == expected_csp, f"req-003 injected_csp is incorrect. Expected: {expected_csp}"