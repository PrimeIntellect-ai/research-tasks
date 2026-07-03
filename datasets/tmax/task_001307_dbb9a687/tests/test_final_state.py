# test_final_state.py

import os
import json
import re
import requests
import pytest

def test_service_redirects():
    base_url = "http://127.0.0.1:8080/login"

    try:
        # Test 1: Valid relative redirect
        r1 = requests.get(base_url, params={"next": "/profile"}, allow_redirects=False, timeout=2)
        assert r1.status_code == 302, f"Expected 302 for relative path, got {r1.status_code}"
        assert r1.headers.get("Location") == "/profile", f"Expected Location: /profile, got {r1.headers.get('Location')}"

        # Test 2: Absolute URL redirect (http)
        r2 = requests.get(base_url, params={"next": "http://evil.com"}, allow_redirects=False, timeout=2)
        assert r2.status_code == 302, f"Expected 302 for absolute URL, got {r2.status_code}"
        assert r2.headers.get("Location") == "/dashboard", f"Expected Location: /dashboard for absolute URL, got {r2.headers.get('Location')}"

        # Test 3: Protocol-relative redirect
        r3 = requests.get(base_url, params={"next": "//evil.com"}, allow_redirects=False, timeout=2)
        assert r3.status_code == 302, f"Expected 302 for protocol-relative URL, got {r3.status_code}"
        assert r3.headers.get("Location") == "/dashboard", f"Expected Location: /dashboard for protocol-relative URL, got {r3.headers.get('Location')}"

        # Test 4: Missing next parameter
        r4 = requests.get(base_url, allow_redirects=False, timeout=2)
        assert r4.status_code == 302, f"Expected 302 for missing next param, got {r4.status_code}"
        assert r4.headers.get("Location") == "/dashboard", f"Expected Location: /dashboard for missing next param, got {r4.headers.get('Location')}"

    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the service at 127.0.0.1:8080. Ensure it is running.")

def test_audit_trail_json():
    log_path = "/home/user/historical_access.log"
    json_path = "/home/user/redirect_audit.json"

    assert os.path.isfile(json_path), f"Audit trail file not found at {json_path}"

    with open(json_path, 'r') as f:
        try:
            audit_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Audit trail is not valid JSON")

    assert isinstance(audit_data, list), "Audit trail must be a JSON array"

    expected = []
    with open(log_path, 'r') as f:
        for line in f:
            # Parse Nginx combined format
            match = re.search(r'^(\S+) \S+ \S+ \[([^\]]+)\] "GET /login\?next=(http[s]?://[^ ]+) HTTP/[0-9.]+" (200|302) ', line)
            if match:
                ip_address = match.group(1)
                timestamp = match.group(2)
                malicious_target = match.group(3)
                expected.append({
                    "timestamp": timestamp,
                    "ip_address": ip_address,
                    "malicious_target": malicious_target
                })

    assert len(audit_data) == len(expected), f"Expected {len(expected)} records, found {len(audit_data)}"

    for exp in expected:
        assert exp in audit_data, f"Missing expected record in audit trail: {exp}"