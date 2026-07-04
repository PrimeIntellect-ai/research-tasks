# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/audit_configs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_csv_exists():
    csv_path = "/home/user/verified_changes.csv"
    assert os.path.isfile(csv_path), f"Output CSV {csv_path} does not exist."

def test_csv_content():
    csv_path = "/home/user/verified_changes.csv"
    assert os.path.isfile(csv_path), f"Output CSV {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Ticket,Filename,Status",
        "TKT-1001,router_v1.bin,Valid",
        "TKT-1001,router_v2.bin,Corrupt",
        "TKT-1002,firewall_v2.bin,Valid",
        "TKT-1002,missing_fw.bin,Missing",
        "TKT-1004,proxy_v1.bin,Corrupt",
        "TKT-1004,switch_v1.bin,Valid"
    ]

    assert len(lines) > 0, "CSV file is empty."
    assert lines[0] == expected_lines[0], f"CSV header is incorrect. Expected '{expected_lines[0]}', got '{lines[0]}'."

    # Check that TKT-1003 is not in the output (it was Rejected)
    for line in lines:
        assert "TKT-1003" not in line, "Rejected ticket TKT-1003 should not be in the output."

    assert lines == expected_lines, "CSV content does not match the expected output or is not sorted correctly."