# test_final_state.py

import os
import re
import subprocess
import pytest

def get_true_malicious_ips():
    """Extract the original access.log from the zip file and parse it to find true malicious IPs."""
    zip_path = "/home/user/infra.zip"
    password = "R0tateMe2024!"

    # Try to extract access.log from the zip file to memory
    result = subprocess.run(
        ["unzip", "-p", "-P", password, zip_path, "*access.log"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0 or not result.stdout:
        # Fallback to the extracted file if zip extraction fails for some reason
        log_path = "/home/user/infra/access.log"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                content = f.read()
        else:
            return set()
    else:
        content = result.stdout

    malicious_ips = set()
    for line in content.splitlines():
        # Directory traversal patterns
        if "../" in line or "%2e%2e%2f" in line.lower():
            # Standard access log: IP is usually the first token
            parts = line.split()
            if parts:
                malicious_ips.add(parts[0])

    return malicious_ips

def test_security_hardening_score():
    """
    Calculates the Security Hardening F1 & Compliance Score and asserts it meets the threshold.
    """
    total_score = 0.0

    # 1. ssh_score (0.33 points)
    ssh_score = 0.0
    ssh_config_path = "/home/user/infra/ssh_config"
    key_path = "/home/user/infra/id_ed25519"

    if os.path.exists(ssh_config_path) and os.path.exists(key_path):
        with open(ssh_config_path, "r") as f:
            ssh_config = f.read()

        has_no_password = re.search(r"^\s*PasswordAuthentication\s+no\b", ssh_config, re.MULTILINE | re.IGNORECASE)
        has_identity_file = re.search(r"^\s*IdentityFile\s+(?:\"?/home/user/infra/id_ed25519\"?|/home/user/infra/id_ed25519)\b", ssh_config, re.MULTILINE)

        if has_no_password and has_identity_file:
            ssh_score = 0.33

    total_score += ssh_score

    # 2. csp_score (0.33 points)
    csp_score = 0.0
    nginx_config_path = "/home/user/infra/nginx.conf"

    if os.path.exists(nginx_config_path):
        with open(nginx_config_path, "r") as f:
            nginx_config = f.read()

        # Look for add_header Content-Security-Policy ... ;
        csp_match = re.search(r"add_header\s+Content-Security-Policy\s+[\"'](.*?)[\"']\s*;", nginx_config, re.IGNORECASE)
        if csp_match:
            csp_value = csp_match.group(1).lower()
            if "default-src 'self'" in csp_value and "'unsafe-inline'" not in csp_value and "'unsafe-eval'" not in csp_value:
                csp_score = 0.33

    total_score += csp_score

    # 3. vuln_score (0.34 points)
    vuln_score = 0.0
    banned_ips_path = "/home/user/infra/banned_ips.txt"
    true_ips = get_true_malicious_ips()
    predicted_ips = set()

    if os.path.exists(banned_ips_path):
        with open(banned_ips_path, "r") as f:
            for line in f:
                ip = line.strip()
                if ip:
                    predicted_ips.add(ip)

    if true_ips:
        tp = len(true_ips.intersection(predicted_ips))
        fp = len(predicted_ips - true_ips)
        fn = len(true_ips - predicted_ips)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
            vuln_score = 0.34 * f1

    total_score += vuln_score

    assert total_score >= 0.90, (
        f"Security Hardening F1 & Compliance Score is {total_score:.3f}, which is below the 0.90 threshold. "
        f"Breakdown: SSH={ssh_score:.3f}/0.33, CSP={csp_score:.3f}/0.33, Vuln={vuln_score:.3f}/0.34"
    )