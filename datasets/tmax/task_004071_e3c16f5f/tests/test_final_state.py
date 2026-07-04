# test_final_state.py
import os
import re
import subprocess
import pytest

def test_attacker_ip():
    """Test that the attacker's IP was correctly extracted."""
    path = "/home/user/attacker_ip.txt"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        ip = f.read().strip()
    assert ip == "198.51.100.42", f"Incorrect attacker IP. Expected 198.51.100.42, got {ip}"

def test_sshd_config_fixed():
    """Test that the SSH configuration was properly hardened."""
    path = "/home/user/sshd_config_fixed"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()

    assert re.search(r"^\s*PermitRootLogin\s+no\s*$", content, re.MULTILINE), "Missing or incorrect PermitRootLogin directive"
    assert re.search(r"^\s*PasswordAuthentication\s+no\s*$", content, re.MULTILINE), "Missing or incorrect PasswordAuthentication directive"
    assert re.search(r"^\s*X11Forwarding\s+no\s*$", content, re.MULTILINE), "Missing or incorrect X11Forwarding directive"
    assert re.search(r"^\s*Protocol\s+2\s*$", content, re.MULTILINE), "Missing or incorrect Protocol directive"

def test_redact_pii_script():
    """Test the redaction script accuracy against a generated dataset."""
    script_path = "/home/user/redact_pii.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    # Ensure it's executable, or we can run it via bash

    input_file = "/tmp/hidden_input.txt"
    expected_file = "/tmp/expected_output.txt"
    agent_output_file = "/tmp/agent_output.txt"

    # Define test cases: (input_line, expected_output_line)
    base_lines = [
        ("My SSN is 123-45-6789.", "My SSN is [REDACTED]."),
        ("Call me at 123-456-7890.", "Call me at 123-456-7890."), # Phone number, not SSN
        ("CC: 1234-5678-9012-3456", "CC: [REDACTED]"),
        ("CC: 1234567890123456", "CC: [REDACTED]"),
        ("ID: 12345678901234567", "ID: 12345678901234567"), # 17 digits, not a CC
        ("Fake CC: 1234-5678-9012-345", "Fake CC: 1234-5678-9012-345"), # Incomplete CC
        ("No numbers here.", "No numbers here."),
        ("Multiple: 111-22-3333 and 4444-5555-6666-7777.", "Multiple: [REDACTED] and [REDACTED]."),
        ("Contiguous CC inside text 1234567890123456.", "Contiguous CC inside text [REDACTED]."),
        ("Another test 000-00-0000 9999999999999999", "Another test [REDACTED] [REDACTED]")
    ]

    # Duplicate to create a larger file (10,000 lines)
    lines = base_lines * 1000

    with open(input_file, "w") as f_in, open(expected_file, "w") as f_exp:
        for in_line, exp_line in lines:
            f_in.write(in_line + "\n")
            f_exp.write(exp_line + "\n")

    # Run agent script
    result = subprocess.run(["bash", script_path, input_file, agent_output_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    assert os.path.isfile(agent_output_file), "Agent script did not produce the output file."

    with open(agent_output_file, "r") as f_agent, open(expected_file, "r") as f_exp:
        agent_lines = f_agent.readlines()
        exp_lines = f_exp.readlines()

    total_lines = len(exp_lines)
    assert len(agent_lines) == total_lines, f"Agent output has incorrect number of lines: {len(agent_lines)} instead of {total_lines}"

    correct_lines = sum(1 for a, e in zip(agent_lines, exp_lines) if a == e)
    accuracy = correct_lines / total_lines

    assert accuracy >= 0.98, f"Accuracy {accuracy:.4f} is below threshold 0.98. Correct lines: {correct_lines}/{total_lines}"