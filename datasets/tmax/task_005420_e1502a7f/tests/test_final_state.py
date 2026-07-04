# test_final_state.py

import os
import pytest

def test_forensics_report_exists():
    path = "/home/user/forensics_report.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

def test_forensics_report_content():
    path = "/home/user/forensics_report.txt"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"File {path} does not contain enough lines."

    cn_found = False
    ips_found = False

    expected_cn = "CN: malicious-update-server.local"
    # The IPs sorted numerically
    expected_ips = "IPs: 192.168.1.50,192.168.1.100"

    for line in lines:
        if line == expected_cn:
            cn_found = True
        if line.replace(" ", "") == expected_ips.replace(" ", ""):
            ips_found = True

    assert cn_found, f"Expected to find exactly '{expected_cn}' in {path}"
    assert ips_found, f"Expected to find exactly '{expected_ips}' in {path}"