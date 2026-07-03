# test_final_state.py

import os
import pytest

def test_report_exists():
    """Test that the report file was created."""
    assert os.path.isfile("/home/user/report.txt"), "The file /home/user/report.txt is missing."

def test_report_contents():
    """Test that the report contains the correct extracted information."""
    expected_content = (
        "Attacker Port: 31337\n"
        "ZIP Password: 7392\n"
        "Certificate CN: internal.corp.local"
    )

    with open("/home/user/report.txt", "r") as f:
        content = f.read().strip()

    assert content == expected_content, (
        f"The contents of /home/user/report.txt are incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )