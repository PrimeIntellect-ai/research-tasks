# test_final_state.py
import os
import subprocess
import pytest
import re

def test_bashrc_env_vars():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        content = f.read()

    assert re.search(r"export\s+SSH_PORT\s*=\s*[\"']?9922[\"']?", content), "SSH_PORT=9922 not properly exported in /home/user/.bashrc"
    assert re.search(r"export\s+EMAIL_PORT\s*=\s*[\"']?2525[\"']?", content), "EMAIL_PORT=2525 not properly exported in /home/user/.bashrc"

def test_fw_generator():
    generator_path = "/home/user/fw_generator.py"
    assert os.path.exists(generator_path), f"{generator_path} does not exist."

    env = os.environ.copy()
    env["SSH_PORT"] = "9922"
    env["EMAIL_PORT"] = "2525"

    try:
        subprocess.run(["python3", generator_path], env=env, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"fw_generator.py failed to run: {e.stderr.decode()}")

    rules_path = "/home/user/fw_rules.txt"
    assert os.path.exists(rules_path), f"{rules_path} was not created."

    with open(rules_path, "r") as f:
        content = f.read().strip().split('\n')

    expected_lines = [
        "iptables -A INPUT -p tcp --dport 9922 -j ACCEPT",
        "iptables -A INPUT -p tcp --dport 2525 -j ACCEPT"
    ]

    assert len(content) >= 2, f"{rules_path} does not contain enough lines."
    assert expected_lines[0] in content, f"Missing rule: {expected_lines[0]} in {rules_path}"
    assert expected_lines[1] in content, f"Missing rule: {expected_lines[1]} in {rules_path}"

def test_detector_script():
    detector_path = "/home/user/detector.py"
    assert os.path.exists(detector_path), f"{detector_path} does not exist."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run(["python3", detector_path, cf], capture_output=True, text=True)
        if res.stdout.strip() != "CLEAN":
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run(["python3", detector_path, ef], capture_output=True, text=True)
        if res.stdout.strip() != "EVIL":
            evil_failures.append(os.path.basename(ef))

    err_msg = []
    if evil_failures:
        err_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        err_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    if err_msg:
        pytest.fail(" | ".join(err_msg))

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/var/log/mail.log" in content, "/var/log/mail.log not specified in logrotate.conf"

    assert re.search(r"\bdaily\b", content), "Directive 'daily' missing in logrotate.conf"
    assert re.search(r"\brotate\s+7\b", content), "Directive 'rotate 7' missing in logrotate.conf"
    assert re.search(r"\bcompress\b", content), "Directive 'compress' missing in logrotate.conf"
    assert re.search(r"\bmissingok\b", content), "Directive 'missingok' missing in logrotate.conf"