# test_final_state.py

import os
import json
import subprocess
import ast
import pytest

BASE_DIR = "/home/user/incident_response"

def test_phase1_cracked_passwords():
    """Verify Phase 1: Passwords cracked and correctly formatted in JSON."""
    output_file = os.path.join(BASE_DIR, "cracked_passwords.json")
    assert os.path.isfile(output_file), f"Phase 1 output file is missing: {output_file}"

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    expected = {"alice": "admin123", "bob": "company2023!"}
    assert data == expected, f"Cracked passwords JSON content is incorrect. Expected {expected}, got {data}"

def test_phase2_app_patched():
    """Verify Phase 2: Vulnerabilities in app.py are remediated."""
    app_path = os.path.join(BASE_DIR, "auth_service", "app.py")
    assert os.path.isfile(app_path), f"Phase 2 app.py file is missing: {app_path}"

    with open(app_path, 'r') as f:
        source = f.read()

    # Check for SQL Injection remediation
    # The original used an f-string: f"SELECT ... '{username}' ..."
    # We expect parameterized queries, which means no string formatting/concatenation for the query.
    tree = ast.parse(source)

    execute_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                execute_calls.append(node)

    assert len(execute_calls) > 0, "No cursor.execute() found in app.py"

    for call in execute_calls:
        # The first argument to execute() should be a string literal, not a JoinedStr (f-string) or BinOp (%)
        if len(call.args) > 0:
            query_arg = call.args[0]
            assert not isinstance(query_arg, ast.JoinedStr), "SQL Injection vulnerability still present: f-string used in cursor.execute()"
            assert not isinstance(query_arg, ast.BinOp), "SQL Injection vulnerability still present: string formatting used in cursor.execute()"
            assert not (isinstance(query_arg, ast.Call) and isinstance(query_arg.func, ast.Attribute) and query_arg.func.attr == 'format'), "SQL Injection vulnerability still present: .format() used in cursor.execute()"

    # Check for Open Redirect remediation
    # The application should validate that next_url starts with '/' and does not contain '//' or absolute URLs.
    # We can check if the source code contains checks for these conditions.
    assert "startswith" in source and "'/'" in source, "Open Redirect vulnerability still present: missing check for relative path (startswith('/'))"
    assert "'//'" in source, "Open Redirect vulnerability still present: missing check to prevent protocol-relative URLs (//)"

def test_phase3_token_rotated():
    """Verify Phase 3: Master token is correctly re-encrypted with new key and IV."""
    rotated_token_path = os.path.join(BASE_DIR, "tokens", "master_token_rotated.enc")
    new_key_path = os.path.join(BASE_DIR, "keys", "new_key.bin")
    new_iv_path = os.path.join(BASE_DIR, "keys", "new_iv.bin")

    assert os.path.isfile(rotated_token_path), f"Phase 3 output file is missing: {rotated_token_path}"
    assert os.path.isfile(new_key_path), f"New key file is missing: {new_key_path}"
    assert os.path.isfile(new_iv_path), f"New IV file is missing: {new_iv_path}"

    # Read key and IV as hex for openssl
    with open(new_key_path, 'rb') as f:
        new_key_hex = f.read().hex()
    with open(new_iv_path, 'rb') as f:
        new_iv_hex = f.read().hex()

    # Decrypt the rotated token using openssl
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-in", rotated_token_path,
        "-K", new_key_hex,
        "-iv", new_iv_hex
    ]

    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode == 0, f"Failed to decrypt rotated token. OpenSSL error: {result.stderr.decode()}"

    decrypted_token = result.stdout.decode('utf-8')
    expected_token = "SuperSecretMasterToken999"
    assert decrypted_token == expected_token, f"Decrypted token does not match expected value. Got: {decrypted_token}"

def test_phase4_invalid_cert_identified():
    """Verify Phase 4: Invalid certificate Common Name is correctly identified."""
    output_file = os.path.join(BASE_DIR, "invalid_cert_cn.txt")
    assert os.path.isfile(output_file), f"Phase 4 output file is missing: {output_file}"

    with open(output_file, 'r') as f:
        cn = f.read().strip()

    expected_cn = "Compromised-Intermediate-CA"
    assert cn == expected_cn, f"Invalid certificate CN incorrect. Expected '{expected_cn}', got '{cn}'"