# test_final_state.py

import os
import pytest

def test_sqli_ips_file_exists():
    """Test that the output file exists."""
    path = "/home/user/sqli_ips.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The task is incomplete."

def test_sqli_ips_content():
    """Test that the output file contains the correct IP addresses."""
    path = "/home/user/sqli_ips.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected_ips = {
        "10.0.0.51",
        "10.0.0.202",
        "203.0.113.42"
    }

    with open(path, "r") as f:
        lines = f.readlines()

    actual_ips = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            actual_ips.append(stripped)

    # Check for extra lines or missing lines
    assert len(actual_ips) == len(expected_ips), f"Expected {len(expected_ips)} IPs, but found {len(actual_ips)} in {path}."

    # Check if the extracted IPs match the expected ones (ignoring order)
    assert set(actual_ips) == expected_ips, f"The IPs in {path} do not match the expected SQLi_Attempt IPs."