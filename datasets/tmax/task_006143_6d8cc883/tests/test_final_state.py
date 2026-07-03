# test_final_state.py

import os
import json
import pytest

def test_aliases_file_content():
    path = '/home/user/aliases'
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "list-admin: admin@localdomain.internal",
        "list-alice: alice@localdomain.internal",
        "list-bob: bob@localdomain.internal"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {path}"

    assert len(lines) == len(expected_lines), f"File {path} contains unexpected or duplicate lines. Found {len(lines)} lines, expected {len(expected_lines)}."

def test_firewall_rules_file_content():
    path = '/home/user/firewall.rules'
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "-A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-ports 2525",
        "-A PREROUTING -p tcp --dport 8081 -j REDIRECT --to-ports 2525",
        "-A PREROUTING -p tcp --dport 8082 -j REDIRECT --to-ports 2525"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {path}"

    assert len(lines) == len(expected_lines), f"File {path} contains unexpected or duplicate lines. Found {len(lines)} lines, expected {len(expected_lines)}."

def test_update_users_script_absolute_paths():
    path = '/home/user/update_users.py'
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, 'r') as f:
        content = f.read()

    assert "'/home/user/user_db.json'" in content or '"/home/user/user_db.json"' in content, "Script does not use absolute path for user_db.json"
    assert "'/home/user/aliases'" in content or '"/home/user/aliases"' in content, "Script does not use absolute path for aliases"
    assert "'/home/user/firewall.rules'" in content or '"/home/user/firewall.rules"' in content, "Script does not use absolute path for firewall.rules"

def test_idempotency_no_duplicates():
    aliases_path = '/home/user/aliases'
    firewall_path = '/home/user/firewall.rules'

    with open(aliases_path, 'r') as f:
        aliases_lines = [line.strip() for line in f if line.strip()]
    assert len(aliases_lines) == len(set(aliases_lines)), f"Duplicate lines found in {aliases_path}, script is not idempotent."

    with open(firewall_path, 'r') as f:
        firewall_lines = [line.strip() for line in f if line.strip()]
    assert len(firewall_lines) == len(set(firewall_lines)), f"Duplicate lines found in {firewall_path}, script is not idempotent."