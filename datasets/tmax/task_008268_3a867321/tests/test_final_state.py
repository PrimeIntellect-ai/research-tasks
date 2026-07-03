# test_final_state.py

import os
import re

def test_crack_go_exists():
    """Verify that the crack.go file exists."""
    assert os.path.isfile("/home/user/crack.go"), "/home/user/crack.go is missing"

def test_remediate_sh():
    """Verify that remediate.sh exists and contains the correct iptables command."""
    file_path = "/home/user/remediate.sh"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, "r") as f:
        content = f.read()

    # Check for essential components of the iptables command
    assert "iptables" in content, "iptables command missing in remediate.sh"

    # Check for append to INPUT
    assert re.search(r'-(A|-append)\s+INPUT', content), "iptables rule must append to INPUT chain"

    # Check for protocol tcp
    assert re.search(r'-(p|-protocol)\s+tcp', content), "iptables rule must specify tcp protocol"

    # Check for port 13337
    assert re.search(r'--dport\s+13337', content) or re.search(r'--destination-port\s+13337', content), "iptables rule must specify destination port 13337"

    # Check for DROP jump
    assert re.search(r'-(j|-jump)\s+DROP', content), "iptables rule must jump to DROP"

def test_report_txt():
    """Verify that report.txt contains the correct findings."""
    file_path = "/home/user/report.txt"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "PIN: 4829\nPORT: 13337\nTAMPERED_BINARY: service_beta"

    # Normalize line endings and strip whitespace
    normalized_content = "\n".join(line.strip() for line in content.splitlines() if line.strip())

    assert normalized_content == expected_content, f"report.txt content is incorrect. Expected:\n{expected_content}\nGot:\n{normalized_content}"