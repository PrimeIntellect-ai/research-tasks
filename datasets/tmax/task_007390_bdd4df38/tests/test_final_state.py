# test_final_state.py

import os
import pytest

def test_report_exists_and_correct():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, but got {len(lines)}."

    expected_ip_line = "Attacker IP: 192.168.1.105"
    expected_password_line = "Cracked Password: cyberdragon"

    assert lines[0] == expected_ip_line, f"First line is incorrect. Expected '{expected_ip_line}', got '{lines[0]}'."
    assert lines[1] == expected_password_line, f"Second line is incorrect. Expected '{expected_password_line}', got '{lines[1]}'."