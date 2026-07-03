# test_final_state.py

import os
import json
import pytest

def weak_hash(data: bytes) -> int:
    """Python implementation of the Rust weak_hash function."""
    hash_val = 0
    for i, b in enumerate(data):
        hash_val = (hash_val + b * (i + 1)) % (2**32)
    return hash_val

def test_open_port_correct():
    """Validates that open_port.txt contains the correct port derived from firewall_rules.json."""
    rules_file = "/home/user/audit/firewall_rules.json"
    port_file = "/home/user/audit/open_port.txt"

    assert os.path.exists(rules_file), f"Missing {rules_file}"
    with open(rules_file, "r") as f:
        try:
            rules = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{rules_file} is not valid JSON")

    expected_port = None
    for policy in rules.get("policies", []):
        if policy.get("service") == "internal_file_server":
            expected_port = policy.get("port")
            break

    assert expected_port is not None, "Could not find 'internal_file_server' policy in firewall_rules.json to derive the expected port."

    assert os.path.exists(port_file), f"Missing {port_file}. The task requires writing the port number to this file."
    with open(port_file, "r") as f:
        actual_port = f.read().strip()

    assert actual_port == str(expected_port), f"Expected port {expected_port} in {port_file}, but found '{actual_port}'."

def test_csp_header_in_server():
    """Validates that the correct Content-Security-Policy header was added to server.rs."""
    server_file = "/home/user/audit/server.rs"
    assert os.path.exists(server_file), f"Missing {server_file}"

    with open(server_file, "r") as f:
        content = f.read()

    expected_header = "Content-Security-Policy: default-src 'self'; script-src 'none';"
    assert expected_header in content, (
        f"The required CSP header '{expected_header}' was not found in {server_file}."
    )

def test_forged_config_collision():
    """Validates the cryptanalysis task by checking the forged file's prefix and hash collision."""
    forged_file = "/home/user/audit/forged_config.txt"
    assert os.path.exists(forged_file), f"Missing {forged_file}. The forged configuration file must be created."

    with open(forged_file, "rb") as f:
        forged_data = f.read()

    # Check the prefix
    expected_prefix = b"role=admin"
    assert forged_data.startswith(expected_prefix), (
        f"The forged config must start with exactly '{expected_prefix.decode()}', "
        f"but it started with '{forged_data[:10]}'."
    )

    # Calculate the target hash dynamically
    target_data = b"role=standard_user"
    target_hash = weak_hash(target_data)

    # Calculate the forged hash
    forged_hash = weak_hash(forged_data)

    assert forged_hash == target_hash, (
        f"Hash collision failed. Expected hash {target_hash} (derived from '{target_data.decode()}'), "
        f"but the forged file produced hash {forged_hash}."
    )