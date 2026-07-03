# test_final_state.py

import os
import re

def test_recovered_cookies_accuracy():
    """
    Evaluate the accuracy of the recovered cookies against the ground truth.
    The accuracy must be >= 0.95 (95%).
    """
    truth_path = "/app/truth/golden_cookies.txt"
    agent_path = "/home/user/recovered_cookies.txt"

    assert os.path.exists(agent_path), f"Agent output file missing: {agent_path}"

    with open(truth_path, 'r') as f:
        truth_lines = [l.strip() for l in f.readlines() if l.strip()]

    with open(agent_path, 'r') as f:
        agent_lines = [l.strip() for l in f.readlines() if l.strip()]

    assert len(truth_lines) > 0, "Ground truth file is empty."

    correct = 0
    for t in truth_lines:
        if t in agent_lines:
            correct += 1

    accuracy = correct / len(truth_lines)

    assert accuracy >= 0.95, f"Recovered cookies accuracy {accuracy:.4f} is below the 0.95 threshold."

def test_block_attacker_script():
    """
    Verify that the block_attacker.sh script contains the correct iptables command
    to drop incoming TCP traffic from the attacker's IP (192.168.1.55).
    """
    script_path = "/home/user/block_attacker.sh"

    assert os.path.exists(script_path), f"Bash script missing: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for key components of the iptables command
    assert "iptables" in content, "iptables command not found in the script."
    assert "192.168.1.55" in content, "Attacker IP 192.168.1.55 not found in the script."
    assert "-p tcp" in content or "--protocol tcp" in content, "TCP protocol flag missing."
    assert "-j DROP" in content or "--jump DROP" in content, "DROP target missing."

    # Check for INPUT chain insertion/append
    assert "-A INPUT" in content or "-I INPUT" in content or "--append INPUT" in content or "--insert INPUT" in content, "INPUT chain rule missing."