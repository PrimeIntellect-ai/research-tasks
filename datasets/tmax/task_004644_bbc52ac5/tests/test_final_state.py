# test_final_state.py

import os
import re
import pytest

def test_analyze_agent_script_exists():
    """Test that the python script analyze_agent.py exists."""
    script_path = "/home/user/analyze_agent.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_audit_trail_log_exists():
    """Test that the audit_trail.log file exists."""
    log_path = "/home/user/audit_trail.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

def test_audit_trail_log_content():
    """Test that the audit_trail.log contains the correct extracted information."""
    log_path = "/home/user/audit_trail.log"

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for specific lines
    expected_ip_line = "[AUDIT] Embedded IP: 203.0.113.85"
    expected_subject_line = "[AUDIT] Cert Subject: legacy-audit.local"
    expected_block_line = "[AUDIT] Block Command: iptables -A OUTPUT -d 203.0.113.85 -j DROP"

    assert expected_ip_line in content, f"Expected line '{expected_ip_line}' not found in {log_path}."
    assert expected_subject_line in content, f"Expected line '{expected_subject_line}' not found in {log_path}."
    assert expected_block_line in content, f"Expected line '{expected_block_line}' not found in {log_path}."

    # Check for the expiry date format
    expiry_pattern = r"\[AUDIT\] Cert Expiry: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    assert re.search(expiry_pattern, content) is not None, (
        f"Expected expiry date line matching pattern '{expiry_pattern}' not found in {log_path}."
    )