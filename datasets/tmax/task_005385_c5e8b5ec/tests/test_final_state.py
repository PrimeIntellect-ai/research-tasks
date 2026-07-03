# test_final_state.py

import os
import stat
import json
import pytest
import subprocess

def test_audit_py_exists():
    script_path = "/home/user/audit.py"
    assert os.path.exists(script_path), f"File {script_path} is missing."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

def test_vulnerable_tokens_exists_and_permissions():
    output_file = "/home/user/vulnerable_tokens.json"
    assert os.path.exists(output_file), f"File {output_file} is missing."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    # Check permissions 0400
    file_stat = os.stat(output_file)
    # Mask out the file type bits, keep only permission bits
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o400, f"Permissions of {output_file} are {oct(permissions)}, expected 0o400."

def test_vulnerable_tokens_content():
    output_file = "/home/user/vulnerable_tokens.json"
    assert os.path.exists(output_file), f"File {output_file} is missing."

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Content of {output_file} is not valid JSON.")

    expected_tokens = [
        "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTYxNjIzOTAyMn0.",
        "eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJyb290IiwiaWF0IjoxNjE2MjM5MDIyfQ."
    ]

    assert isinstance(data, list), f"Expected a JSON array in {output_file}, but got {type(data).__name__}."
    assert data == expected_tokens, f"Content of {output_file} does not match the expected vulnerable tokens."

def test_ssh_keypair_exists_and_valid():
    private_key = "/home/user/new_jwt_key"
    public_key = "/home/user/new_jwt_key.pub"

    assert os.path.exists(private_key), f"Private key {private_key} is missing."
    assert os.path.isfile(private_key), f"Path {private_key} is not a file."

    assert os.path.exists(public_key), f"Public key {public_key} is missing."
    assert os.path.isfile(public_key), f"Path {public_key} is not a file."

    # Check if it's a valid ED25519 key using ssh-keygen
    try:
        result = subprocess.run(
            ["ssh-keygen", "-l", "-f", private_key],
            capture_output=True, text=True, check=True
        )
        assert "ED25519" in result.stdout.upper(), "The generated SSH key is not an ED25519 key."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ssh-keygen failed to validate the private key: {e.stderr}")