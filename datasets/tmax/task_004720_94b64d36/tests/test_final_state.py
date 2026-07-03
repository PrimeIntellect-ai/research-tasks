# test_final_state.py

import os
import pytest

def test_extracted_payloads_exists():
    """Verify that the extracted_payloads.txt file exists."""
    payloads_path = "/home/user/ticket_8841/extracted_payloads.txt"
    assert os.path.isfile(payloads_path), f"File {payloads_path} is missing. Did you extract the payloads?"

def test_final_averages_exists():
    """Verify that the final_averages.txt file exists."""
    averages_path = "/home/user/ticket_8841/final_averages.txt"
    assert os.path.isfile(averages_path), f"File {averages_path} is missing. Did you run the fixed script?"

def test_final_averages_content():
    """Verify the content and formatting of final_averages.txt."""
    averages_path = "/home/user/ticket_8841/final_averages.txt"
    if not os.path.isfile(averages_path):
        pytest.fail(f"Cannot check content because {averages_path} is missing.")

    with open(averages_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Expected values based on the pcap payloads:
    # S1: (10.50 + 15.75) / 2 = 13.125
    # S2: (20.25 + 30.75) / 2 = 25.50
    # S3: (100.00 + 100.05) / 2 = 100.025

    expected_s1 = ["S1:13.12", "S1:13.13"]
    expected_s2 = ["S2:25.50"]
    expected_s3 = ["S3:100.02", "S3:100.03"]

    # Check that there are exactly 3 lines (one for each valid sensor)
    assert len(lines) == 3, f"Expected exactly 3 lines in {averages_path}, but found {len(lines)}. Make sure malformed data is skipped."

    # Check sorting and exact values
    assert lines[0] in expected_s1, f"Line 1 expected to be one of {expected_s1}, got '{lines[0]}'"
    assert lines[1] in expected_s2, f"Line 2 expected to be one of {expected_s2}, got '{lines[1]}'"
    assert lines[2] in expected_s3, f"Line 3 expected to be one of {expected_s3}, got '{lines[2]}'"