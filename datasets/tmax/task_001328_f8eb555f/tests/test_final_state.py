# test_final_state.py

import os
import json
import pytest

def test_nfs_mounts_log():
    log_path = "/home/user/nfs_mounts.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the script generate it?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_mounts = [
        "/mnt/shared_nfs",
        "/opt/app_data"
    ]

    assert lines == expected_mounts, f"Content of {log_path} does not match the expected NFS mount points. Expected {expected_mounts}, but got {lines}."

def test_iptables_sh():
    script_path = "/home/user/iptables.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist. Did the script generate it?"

    with open(script_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "#!/bin/bash",
        "iptables -A INPUT -s 192.168.1.50 -j DROP",
        "iptables -A INPUT -s 10.5.5.1 -j DROP",
        "iptables -A INPUT -s 172.16.0.4 -j DROP"
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, f"Content of {script_path} does not match the expected iptables commands. Please check the shebang and the rule format."

def test_app_restarts_log():
    log_path = "/home/user/app_restarts.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the script catch the crashes and generate the log?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Crash detected. Exit code: 3",
        "Crash detected. Exit code: 12",
        "Crash detected. Exit code: 7"
    ]

    assert lines == expected_lines, f"Content of {log_path} does not match the expected crash logs. Expected {expected_lines}, but got {lines}."