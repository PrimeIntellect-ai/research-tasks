# test_final_state.py
import os
import json
import hashlib
import re

def test_block_ips_script():
    script_path = "/home/user/block_ips.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert content.startswith("#!/bin/bash"), f"Script {script_path} does not start with #!/bin/bash."

    expected_ips = ["203.0.113.42", "198.51.100.17", "192.0.2.215"]
    for ip in expected_ips:
        # Look for something like: iptables -A INPUT -s <ip> -j DROP
        pattern = rf"iptables\s+-A\s+INPUT\s+-s\s+{re.escape(ip)}\s+-j\s+DROP"
        assert re.search(pattern, content), f"Script missing or incorrect iptables rule for IP {ip}."

def test_audit_report():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    binary_path = "/home/user/suspicious_web_worker.elf"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing."

    with open(binary_path, "rb") as f:
        actual_md5 = hashlib.md5(f.read()).hexdigest()

    assert "elf_md5" in data, "Missing 'elf_md5' in audit report."
    assert data["elf_md5"] == actual_md5, f"Expected MD5 {actual_md5}, got {data['elf_md5']}."

    expected_ips = ["203.0.113.42", "198.51.100.17", "192.0.2.215"]
    assert "extracted_ips" in data, "Missing 'extracted_ips' in audit report."
    assert isinstance(data["extracted_ips"], list), "'extracted_ips' must be a list."
    assert set(data["extracted_ips"]) == set(expected_ips), f"Expected IPs {expected_ips}, got {data['extracted_ips']}."

    assert "firewall_script" in data, "Missing 'firewall_script' in audit report."
    assert data["firewall_script"] == "/home/user/block_ips.sh", "Incorrect 'firewall_script' path in audit report."