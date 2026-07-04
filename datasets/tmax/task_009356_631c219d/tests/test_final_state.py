# test_final_state.py
import os
import stat
import pytest

def test_apply_fw_script():
    script_path = "/home/user/apply_fw.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Check if executable
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "#!/bin/bash",
        "iptables -I INPUT -p tcp --dport 4444 -j DROP",
        "iptables -I INPUT -p tcp --dport 8080 -j DROP",
        "iptables -I INPUT -p tcp --dport 31337 -j DROP"
    ]

    assert content == expected_lines, f"{script_path} content does not match expected output."

def test_bashrc_configured():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "export SEC_HARDENED=true" in content, f"{bashrc_path} does not contain 'export SEC_HARDENED=true'."

def test_quarantine_directory_and_files():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Directory {quarantine_dir} does not exist."

    quarantined_files = [
        "server.conf",
        "api.conf"
    ]

    for filename in quarantined_files:
        filepath = os.path.join(quarantine_dir, filename)
        assert os.path.isfile(filepath), f"Quarantined file {filepath} does not exist."

        # Check permissions
        mode = os.stat(filepath).st_mode
        perms = stat.S_IMODE(mode)
        assert perms == 0o000, f"Permissions for {filepath} are not 000 (found {oct(perms)})."

def test_original_files_removed():
    removed_files = [
        "/home/user/app_data/sub1/server.conf",
        "/home/user/app_data/sub2/api.conf"
    ]
    for filepath in removed_files:
        assert not os.path.exists(filepath), f"Vulnerable file {filepath} was not moved/removed."

def test_safe_files_remain():
    safe_files = [
        "/home/user/app_data/safe.txt",
        "/home/user/app_data/sub1/secure.conf"
    ]
    for filepath in safe_files:
        assert os.path.isfile(filepath), f"Safe file {filepath} is missing. It should not have been moved."