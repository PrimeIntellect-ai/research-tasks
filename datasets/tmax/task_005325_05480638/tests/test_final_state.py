# test_final_state.py

import os
import pytest

def test_process_traffic_script_exists():
    """Test that the process_traffic.py script was created."""
    script_path = "/home/user/process_traffic.py"
    assert os.path.exists(script_path), f"Missing required script: {script_path}"
    assert os.path.isfile(script_path), f"{script_path} should be a file"

def test_redacted_payloads_correct():
    """Test that redacted_payloads.txt contains the correctly redacted bodies."""
    output_path = "/home/user/redacted_payloads.txt"
    assert os.path.exists(output_path), f"Missing required output file: {output_path}"

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "User data: SSN 123-45-REDACTED found.",
        "More data, SSN 555-66-REDACTED and 888-99-REDACTED."
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_path}, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nGot: {actual}"

def test_block_c2_script_valid():
    """Test that block_c2.sh is executable and contains the correct iptables command."""
    script_path = "/home/user/block_c2.sh"
    assert os.path.exists(script_path), f"Missing required script: {script_path}"
    assert os.path.isfile(script_path), f"{script_path} should be a file"

    # Check if executable
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable. Did you run chmod +x?"

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for required components of the iptables command
    assert "iptables" in content, f"Script {script_path} must contain 'iptables' command"
    assert "OUTPUT" in content, f"Script {script_path} must target the 'OUTPUT' chain"
    assert "203.0.113.88" in content, f"Script {script_path} must target the C2 IP '203.0.113.88'"
    assert "DROP" in content, f"Script {script_path} must 'DROP' the traffic"