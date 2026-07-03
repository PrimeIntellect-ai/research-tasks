# test_final_state.py

import os
import json
import base64
import gzip
import pytest

def test_analysis_directory_exists():
    """Verify that the analysis directory was created."""
    assert os.path.isdir("/home/user/analysis"), "The directory /home/user/analysis/ was not created."

def test_malware_py_decoded_correctly():
    """Verify that the malware payload was correctly decoded and decompressed."""
    malware_path = "/home/user/analysis/malware.py"
    payload_path = "/home/user/incident_data/intercepted_payload.txt"

    assert os.path.isfile(malware_path), f"The file {malware_path} is missing."
    assert os.path.isfile(payload_path), f"The file {payload_path} is missing."

    with open(payload_path, "r") as f:
        b64_payload = f.read().strip()

    compressed_payload = base64.b64decode(b64_payload)
    expected_malware_content = gzip.decompress(compressed_payload).decode('utf-8')

    with open(malware_path, "r") as f:
        actual_malware_content = f.read()

    assert actual_malware_content == expected_malware_content, "The content of malware.py does not match the decoded payload."

def test_cwe_identification():
    """Verify that the correct CWE was identified."""
    cwe_path = "/home/user/analysis/cwe.txt"
    assert os.path.isfile(cwe_path), f"The file {cwe_path} is missing."

    with open(cwe_path, "r") as f:
        cwe_content = f.read().strip()

    assert cwe_content == "CWE-78", f"Expected CWE-78, but found '{cwe_content}' in {cwe_path}."

def test_c2_info_extraction():
    """Verify that the C2 info was correctly extracted and formatted."""
    c2_info_path = "/home/user/analysis/c2_info.txt"
    assert os.path.isfile(c2_info_path), f"The file {c2_info_path} is missing."

    with open(c2_info_path, "r") as f:
        c2_info_content = f.read().strip()

    expected_content = "evil-c2-server.internal,192.168.100.88"
    assert c2_info_content == expected_content, f"Expected '{expected_content}', but found '{c2_info_content}' in {c2_info_path}."

def test_firewall_rule_generation():
    """Verify that the firewall rule was correctly generated."""
    fw_rules_path = "/home/user/analysis/firewall.rules"
    assert os.path.isfile(fw_rules_path), f"The file {fw_rules_path} is missing."

    with open(fw_rules_path, "r") as f:
        fw_rules_content = f.read().strip()

    expected_rule = "iptables -A OUTPUT -d 192.168.100.88 -j DROP"
    assert fw_rules_content == expected_rule, f"Expected '{expected_rule}', but found '{fw_rules_content}' in {fw_rules_path}."