# test_final_state.py

import os
import json
import re
import pytest

def test_report_json():
    report_path = '/home/user/evidence/report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} does not contain valid JSON.")

    assert "cwe_id" in data, "Report JSON is missing the 'cwe_id' key."
    assert data["cwe_id"].upper() == "CWE-601", f"Incorrect CWE ID. Expected CWE-601, got {data['cwe_id']}."

    assert "c2_ip" in data, "Report JSON is missing the 'c2_ip' key."
    assert data["c2_ip"] == "203.0.113.85", f"Incorrect C2 IP. Expected 203.0.113.85, got {data['c2_ip']}."

def test_block_c2_sh():
    script_path = '/home/user/evidence/block_c2.sh'
    assert os.path.isfile(script_path), f"Firewall script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read().strip()

    # Remove extra spaces and newlines for easier matching
    normalized_content = re.sub(r'\s+', ' ', content)

    # Check for essential components of the iptables command
    assert "iptables" in normalized_content, "The script does not contain an 'iptables' command."
    assert "-A OUTPUT" in normalized_content or "--append OUTPUT" in normalized_content, "The rule must append to the OUTPUT chain."
    assert "-d 203.0.113.85" in normalized_content or "--destination 203.0.113.85" in normalized_content, "The rule must specify the correct destination IP."
    assert "-p tcp" in normalized_content or "--protocol tcp" in normalized_content, "The rule must specify the TCP protocol."
    assert "--dport 4444" in normalized_content or "--destination-port 4444" in normalized_content, "The rule must specify destination port 4444."
    assert "-j DROP" in normalized_content or "--jump DROP" in normalized_content, "The rule must DROP the traffic."

def test_app_py_patched():
    app_path = '/home/user/webapp/app.py'
    assert os.path.isfile(app_path), f"Application file {app_path} is missing."

    with open(app_path, 'r') as f:
        content = f.read()

    # Check that the vulnerability has been patched by looking for validation logic
    # The instructions say: "Ensure that the `next` parameter is only followed if it is a relative path
    # (it must start with a single `/` and must NOT start with `//` or `http`)."

    # Check for some form of validation
    has_slash_check = "startswith('/')" in content or "startswith(\"/\")" in content or "next_url[0] == '/'" in content or "next_url[0] == \"/\"" in content
    has_double_slash_check = "startswith('//')" in content or "startswith(\"//\")" in content or "http" in content or "://" in content

    assert has_slash_check, "app.py does not appear to check if next_url starts with '/'."
    assert has_double_slash_check, "app.py does not appear to check against absolute URLs (e.g., '//' or 'http')."

    # Ensure it still redirects
    assert "redirect(" in content, "app.py is missing redirect logic."