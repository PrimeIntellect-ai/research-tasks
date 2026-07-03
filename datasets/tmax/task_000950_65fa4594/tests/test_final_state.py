# test_final_state.py
import json
import urllib.request
import urllib.error
import os
import pytest

def test_waf_behavior():
    evil_tokens_path = "/home/user/test_data/evil_tokens.json"
    clean_tokens_path = "/home/user/test_data/clean_tokens.json"

    assert os.path.exists(evil_tokens_path), f"Missing evil corpus at {evil_tokens_path}"
    assert os.path.exists(clean_tokens_path), f"Missing clean corpus at {clean_tokens_path}"

    with open(evil_tokens_path, 'r') as f:
        evil_tokens = json.load(f)

    with open(clean_tokens_path, 'r') as f:
        clean_tokens = json.load(f)

    evil_bypassed = []
    clean_modified = []

    # Test Evil Tokens
    for idx, token in enumerate(evil_tokens):
        req = urllib.request.Request("http://127.0.0.1:80/api/data")
        req.add_header("Authorization", f"Bearer {token}")
        try:
            urllib.request.urlopen(req, timeout=2)
            evil_bypassed.append(f"evil_token_{idx}")
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_bypassed.append(f"evil_token_{idx} (got {e.code} instead of 403)")
        except Exception as e:
            evil_bypassed.append(f"evil_token_{idx} (unexpected error {e})")

    # Test Clean Tokens
    for idx, token in enumerate(clean_tokens):
        req = urllib.request.Request("http://127.0.0.1:80/api/data")
        req.add_header("Authorization", f"Bearer {token}")
        try:
            resp = urllib.request.urlopen(req, timeout=2)
            if resp.getcode() != 200:
                clean_modified.append(f"clean_token_{idx} (got {resp.getcode()} instead of 200)")
        except urllib.error.HTTPError as e:
            clean_modified.append(f"clean_token_{idx} (got HTTPError {e.code})")
        except Exception as e:
            clean_modified.append(f"clean_token_{idx} (unexpected error {e})")

    err_msg = []
    if evil_bypassed:
        err_msg.append(f"{len(evil_bypassed)} of {len(evil_tokens)} evil bypassed: {evil_bypassed}")
    if clean_modified:
        err_msg.append(f"{len(clean_modified)} of {len(clean_tokens)} clean modified: {clean_modified}")

    if err_msg:
        pytest.fail(" | ".join(err_msg))

def test_waf_logging():
    log_file = "/home/user/logs/waf_blocks.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist. The WAF must log rejected requests."

    with open(log_file, 'r') as f:
        content = f.read()

    assert "REJECTED: IP=" in content, "WAF blocks log does not contain the required 'REJECTED: IP=' format."
    assert "REASON=" in content, "WAF blocks log does not contain the required 'REASON=' format."

def test_services_running():
    # Verify that Nginx, WAF, Flask, and Redis are listening on their respective ports
    import socket

    services = {
        "Nginx": 80,
        "WAF": 8080,
        "Flask": 5000,
        "Redis": 6379
    }

    for name, port in services.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Service {name} is not listening on port {port}."