# test_final_state.py

import os
import pytest

def test_attacker_ip():
    path = "/home/user/attacker_ip.txt"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "203.0.113.88", f"Expected '203.0.113.88', but got '{content}'"

def test_block_ip_script():
    path = "/home/user/block_ip.sh"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, 'r') as f:
        content = f.read().strip()

    assert "iptables" in content, "Missing 'iptables' command in script"
    assert "203.0.113.88" in content, "Missing attacker IP in script"
    assert "-p tcp" in content or "--protocol tcp" in content, "Missing TCP protocol flag in script"
    assert "-j DROP" in content or "--jump DROP" in content, "Missing DROP target in script"
    assert ("-A INPUT" in content or "-I INPUT" in content or 
            "--append INPUT" in content or "--insert INPUT" in content), "Missing INPUT chain rule in script"

def test_check_integrity_c_exists():
    path = "/home/user/check_integrity.c"
    assert os.path.isfile(path), f"File missing: {path}"

def test_tampered_file():
    path = "/home/user/tampered_file.txt"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "/app/webroot/api/users.json", f"Expected '/app/webroot/api/users.json', but got '{content}'"

def test_redact_c_exists():
    path = "/home/user/redact.c"
    assert os.path.isfile(path), f"File missing: {path}"

def test_redacted_dump_accuracy():
    agent_file = "/home/user/redacted_dump.txt"
    golden_file = "/app/golden_redacted_dump.txt"

    assert os.path.isfile(agent_file), f"Agent output missing: {agent_file}"
    assert os.path.isfile(golden_file), f"Golden file missing: {golden_file}"

    with open(agent_file, 'r') as f:
        agent_text = f.read()
    with open(golden_file, 'r') as f:
        golden_text = f.read()

    if len(agent_text) == 0 and len(golden_text) > 0:
        accuracy = 0.0
    else:
        matches = sum(1 for a, b in zip(agent_text, golden_text) if a == b)
        max_len = max(len(agent_text), len(golden_text))
        accuracy = matches / max_len if max_len > 0 else 1.0

    assert accuracy >= 0.99, f"Accuracy {accuracy:.4f} is below threshold 0.99"