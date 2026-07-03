# test_final_state.py

import os
import re
import requests
import pytest

def test_sshd_config_hardened():
    """Verify the SSH hardened configuration file exists and contains the exact required directives."""
    config_path = "/home/user/sshd_config_hardened"
    assert os.path.exists(config_path), f"SSH configuration file missing: {config_path}"
    assert os.path.isfile(config_path), f"Path is not a file: {config_path}"

    with open(config_path, 'r') as f:
        lines = f.readlines()

    # Filter out comments and empty lines
    active_directives = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Normalize whitespace
            normalized_line = re.sub(r'\s+', ' ', line)
            active_directives.append(normalized_line)

    expected_directives = {
        "PermitRootLogin no",
        "PasswordAuthentication no",
        "X11Forwarding no",
        "MaxAuthTries 3",
        "Protocol 2"
    }

    actual_directives = set(active_directives)

    missing = expected_directives - actual_directives
    extra = actual_directives - expected_directives

    assert not missing, f"Missing required SSH directives: {missing}"
    assert not extra, f"Found extra/unauthorized SSH directives: {extra}"

def test_proxy_service_valid_request():
    """Verify the proxy service correctly authorizes a valid request."""
    url = "http://127.0.0.1:8080/scan"

    # Challenge 100, Token f4a4b435 (derived from MASTER_KEY f4a2b9d1)
    headers = {
        "X-Challenge": "100",
        "X-Auth-Token": "f4a4b435"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy service on {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid request, got {response.status_code}"
    assert response.text.strip() == "SCAN_AUTHORIZED", f"Expected body 'SCAN_AUTHORIZED', got '{response.text}'"

def test_proxy_service_invalid_request():
    """Verify the proxy service correctly denies an invalid request."""
    url = "http://127.0.0.1:8080/scan"

    headers = {
        "X-Challenge": "100",
        "X-Auth-Token": "deadbeef"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy service on {url}: {e}")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for invalid request, got {response.status_code}"
    assert response.text.strip() == "ACCESS_DENIED", f"Expected body 'ACCESS_DENIED', got '{response.text}'"

def test_proxy_service_dynamic_challenge():
    """Verify the proxy service correctly computes tokens dynamically for other challenges."""
    url = "http://127.0.0.1:8080/scan"

    # Challenge 42
    # 42 * 1337 = 56154
    # 4104296913 ^ 56154 = 4104344587 -> hex: f4a3740b
    headers = {
        "X-Challenge": "42",
        "X-Auth-Token": "f4a3740b"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to proxy service on {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid dynamic request, got {response.status_code}"
    assert response.text.strip() == "SCAN_AUTHORIZED", f"Expected body 'SCAN_AUTHORIZED', got '{response.text}'"