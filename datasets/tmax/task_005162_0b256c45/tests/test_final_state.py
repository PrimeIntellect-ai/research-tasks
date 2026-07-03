# test_final_state.py

import os
import struct
import pytest

def test_script_exists_and_uses_locking():
    """Check if the disk_analyzer.py script exists and uses fcntl locking."""
    script_path = "/home/user/disk_analyzer.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, "Script is missing 'fcntl.flock'."
    assert "fcntl.LOCK_EX" in content, "Script is missing 'fcntl.LOCK_EX'."

def test_project_totals_csv_content():
    """Check if project_totals.csv has the correctly aggregated data."""
    csv_path = "/home/user/project_totals.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Based on the initial data and the JSON files:
    # Initial: 101: 1000, 104: 500
    # node1: 101: 500, 102: 1500
    # node2: 101: 250, 103: 3000
    # Totals: 101: 1750, 102: 1500, 103: 3000, 104: 500
    expected_lines = [
        "101,1750",
        "102,1500",
        "103,3000",
        "104,500"
    ]

    assert lines == expected_lines, f"CSV content is incorrect. Expected {expected_lines}, got {lines}."

def test_binary_dump_content():
    """Check if the binary dump file has the correctly aggregated data in <IQ format."""
    bin_path = "/home/user/binary_dump.bin"
    assert os.path.isfile(bin_path), f"File {bin_path} does not exist."

    with open(bin_path, "rb") as f:
        data = f.read()

    expected_totals = [
        (101, 1750),
        (102, 1500),
        (103, 3000),
        (104, 500)
    ]

    expected_bytes = b""
    for pid, total in expected_totals:
        expected_bytes += struct.pack("<IQ", pid, total)

    assert len(data) == len(expected_bytes), f"Binary file size is {len(data)} bytes, expected {len(expected_bytes)} bytes."
    assert data == expected_bytes, "Binary file content does not match the expected struct format (<IQ)."