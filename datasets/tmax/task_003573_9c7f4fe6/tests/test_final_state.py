# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_compromised_ip():
    path = "/home/user/compromised_ip.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        ip = f.read().strip()
    assert ip == "203.0.113.42", f"Expected IP '203.0.113.42' in {path}, but got '{ip}'."

def test_exploit_test_sh():
    exploit_path = "/home/user/exploit_test.sh"
    rotator_path = "/home/user/legacy_rotator.sh"

    assert os.path.isfile(exploit_path), f"File {exploit_path} is missing."
    st = os.stat(exploit_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {exploit_path} is not executable."

    # Recreate legacy_rotator.sh in case the student already ran rotate.sh and deleted it
    rotator_content = """#!/bin/bash
# Legacy Credential Rotator v1.0
INPUT=$1
CMD=$2
# Security check
B64_KEY="czNjcjN0X2I0Y2tkMDBy"
SECRET=$(echo "$B64_KEY" | base64 -d)

if [ "$INPUT" == "$SECRET" ]; then
    eval "$CMD"
    exit 0
fi
echo "Rotating credentials..."
"""
    with open(rotator_path, "w") as f:
        f.write(rotator_content)
    os.chmod(rotator_path, 0o755)

    # Run the exploit script
    result = subprocess.run([exploit_path], capture_output=True, text=True)
    output = result.stdout.strip()

    assert output == "SYSTEM_COMPROMISED", f"Expected output 'SYSTEM_COMPROMISED', but got '{output}'."

def test_rotate_sh():
    rotate_path = "/home/user/rotate.sh"
    config_path = "/home/user/config.json"
    rotator_path = "/home/user/legacy_rotator.sh"

    assert os.path.isfile(rotate_path), f"File {rotate_path} is missing."
    st = os.stat(rotate_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {rotate_path} is not executable."

    # Setup environment for rotate.sh
    initial_config = {
        "service": "auth_backend",
        "port": 8080,
        "password": "old_password_123"
    }
    with open(config_path, "w") as f:
        json.dump(initial_config, f, indent=2)

    # Ensure legacy_rotator.sh exists before rotation
    with open(rotator_path, "w") as f:
        f.write("# dummy script\n")

    new_password = "new_secure_pass_999"

    # Run the rotation script
    subprocess.run([rotate_path, new_password], capture_output=True, text=True)

    # Verify config.json
    assert os.path.isfile(config_path), f"File {config_path} is missing after rotation."
    with open(config_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} does not contain valid JSON after rotation.")

    assert data.get("password") == new_password, f"Password in {config_path} was not updated correctly."
    assert data.get("service") == "auth_backend", f"Other JSON fields in {config_path} were altered."
    assert data.get("port") == 8080, f"Other JSON fields in {config_path} were altered."

    # Verify legacy_rotator.sh was deleted
    assert not os.path.exists(rotator_path), f"File {rotator_path} was not deleted by {rotate_path}."