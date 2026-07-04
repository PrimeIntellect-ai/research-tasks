# test_final_state.py
import os
import re
import urllib.parse
import pytest

def get_expected_ips(log_path):
    ips = set()
    if not os.path.exists(log_path):
        return ips

    with open(log_path, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 9:
                continue

            ip = parts[0]
            request = parts[6]
            status = parts[8]

            if status != '302':
                continue

            if not request.startswith('/login'):
                continue

            parsed_url = urllib.parse.urlparse(request)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            if 'next' in query_params:
                next_val = query_params['next'][0]
                if next_val.startswith('http://') or next_val.startswith('https://'):
                    ips.add(ip)
    return sorted(list(ips))

def parse_csp(csp_string):
    directives = {}
    parts = csp_string.split(';')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        tokens = part.split(None, 1)
        if tokens:
            name = tokens[0].lower()
            value = tokens[1] if len(tokens) > 1 else ''
            directives[name] = value
    return directives

def test_ssh_deny_conf():
    """Check if ssh_deny.conf is correctly generated with malicious IPs."""
    log_path = "/home/user/logs/gateway.log"
    conf_path = "/home/user/ssh_deny.conf"

    assert os.path.isfile(conf_path), f"The file {conf_path} was not created."

    expected_ips = get_expected_ips(log_path)
    expected_lines = [f"DenyUsers *@*{ip}" if '*' not in ip else f"DenyUsers *@{ip}" for ip in expected_ips]
    # Actually the format is DenyUsers *@<IP_ADDRESS>
    expected_lines = [f"DenyUsers *@{ip}" for ip in expected_ips]

    with open(conf_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {conf_path} do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_hardened_csp_txt():
    """Check if hardened_csp.txt contains the correct CSP with form-action 'self'."""
    orig_csp_path = "/home/user/csp.txt"
    hardened_csp_path = "/home/user/hardened_csp.txt"

    assert os.path.isfile(hardened_csp_path), f"The file {hardened_csp_path} was not created."

    with open(orig_csp_path, 'r') as f:
        orig_csp = f.read().strip()

    expected_directives = parse_csp(orig_csp)
    expected_directives['form-action'] = "'self'"

    with open(hardened_csp_path, 'r') as f:
        hardened_csp = f.read().strip()

    actual_directives = parse_csp(hardened_csp)

    assert actual_directives == expected_directives, (
        f"The CSP in {hardened_csp_path} does not have the correct directives.\n"
        f"Expected directives: {expected_directives}\n"
        f"Actual directives: {actual_directives}"
    )