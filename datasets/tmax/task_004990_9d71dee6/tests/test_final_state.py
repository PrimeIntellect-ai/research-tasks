# test_final_state.py

import os
import pytest

def test_audit_results_exists():
    """Verify that the audit_results.txt file was created."""
    assert os.path.isfile('/home/user/audit_results.txt'), "The file /home/user/audit_results.txt does not exist."

def test_audit_results_content():
    """Verify that the audit_results.txt file contains the correct output."""
    expected_lines = [
        "backup_id_rsa:0777",
        "config:0755",
        "id_rsa.pub:0666",
        "id_rsa:0644"
    ]

    with open('/home/user/audit_results.txt', 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of /home/user/audit_results.txt do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )