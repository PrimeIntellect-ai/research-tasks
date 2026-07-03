# test_final_state.py
import os
import subprocess
import pytest

def test_cwe_identified():
    path = "/home/user/cwe_identified.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content in ["CWE-347", "CWE-287"], f"Incorrect CWE identified. Found: {content}"

def test_block_rule():
    path = "/home/user/block_rule.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    # Check for essential components of the iptables rule
    assert "iptables" in content, "Missing 'iptables' command in block_rule.txt"
    assert "198.51.100.45" in content, "Missing correct IP address in block_rule.txt"
    assert "-j DROP" in content or "--jump DROP" in content, "Missing DROP action in block_rule.txt"
    assert "-p tcp" in content or "--protocol tcp" in content, "Missing TCP protocol specification in block_rule.txt"

def test_jwt_filter_executable():
    path = "/home/user/jwt_filter.sh"
    assert os.path.isfile(path), f"Missing required file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_jwt_filter_adversarial_corpus():
    script_path = "/home/user/jwt_filter.sh"
    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for filename in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "rb") as f:
            token_data = f.read()

        try:
            result = subprocess.run([script_path], input=token_data, capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_bypassed.append(filename)
        except Exception as e:
            evil_bypassed.append(f"{filename} (error: {str(e)})")

    # Test clean corpus
    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "rb") as f:
            token_data = f.read()

        try:
            result = subprocess.run([script_path], input=token_data, capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_modified.append(filename)
        except Exception as e:
            clean_modified.append(f"{filename} (error: {str(e)})")

    total_evil = len([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])
    total_clean = len([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {total_clean} clean rejected/modified: {', '.join(clean_modified)}")

    assert not error_messages, "Adversarial corpus test failed:\n" + "\n".join(error_messages)