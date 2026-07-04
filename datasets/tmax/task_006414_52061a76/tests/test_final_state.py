# test_final_state.py
import os
import subprocess
import pytest

def test_exploit_jwt_exists_and_valid():
    filepath = "/home/user/auth_service/exploit.jwt"
    assert os.path.isfile(filepath), f"{filepath} does not exist"

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content.count('.') == 2, "Exploit token must have exactly two dots (HEADER.PAYLOAD.SIGNATURE)"

    parts = content.split('.')
    header = parts[0]
    payload = parts[1]

    # The vulnerability checks for "alg":"none" or "alg":"NONE"
    assert "none" in header.lower(), "Exploit header must specify alg=none"
    assert "admin" in payload, "Exploit payload must contain the admin role"

def test_auth_server_compiled_and_patched():
    # Compile the server
    compile_proc = subprocess.run(
        ["make"], 
        cwd="/home/user/auth_service", 
        capture_output=True, 
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation failed: {compile_proc.stderr}"

    executable = "/home/user/auth_service/auth_server"
    assert os.path.isfile(executable), "auth_server executable was not created"

    # Read the exploit token
    with open("/home/user/auth_service/exploit.jwt", 'r') as f:
        exploit_token = f.read().strip()

    # Run the server with the exploit token
    run_proc = subprocess.run(
        [executable, exploit_token],
        capture_output=True,
        text=True
    )

    # The patched server should deny access
    assert run_proc.returncode != 0, "Patched auth_server should exit with a non-zero status when given the exploit token"
    assert "ACCESS DENIED" in run_proc.stdout, "Patched auth_server should output ACCESS DENIED"

def test_cert_chain_validation():
    executable = "/home/user/auth_service/auth_server"
    # Even with a valid signature, the hardcoded depth is 1 in main(), 
    # so the patched verify_cert_chain(depth < 2) should cause it to fail.
    # We pass a token that has a valid signature to bypass the alg=none check and hit the cert check.
    valid_sig_token = '{"alg":"HS256"}.{"role":"user"}.VALID_SIG'

    run_proc = subprocess.run(
        [executable, valid_sig_token],
        capture_output=True,
        text=True
    )

    assert run_proc.returncode != 0, "Patched auth_server should reject tokens if cert chain depth < 2"
    assert "ACCESS DENIED" in run_proc.stdout, "Patched auth_server should output ACCESS DENIED for insufficient cert chain depth"

def test_start_sandboxed_sh():
    filepath = "/home/user/auth_service/start_sandboxed.sh"
    assert os.path.isfile(filepath), f"{filepath} does not exist"
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable"

    with open(filepath, 'r') as f:
        content = f.read()

    assert "bwrap" in content, "Script must use bwrap"
    assert "--ro-bind / /" in content, "Script must bind mount / as read-only"
    assert "--tmpfs /tmp" in content, "Script must provide a tmpfs at /tmp"
    assert "--unshare-all" in content, "Script must unshare all namespaces"
    assert "./auth_server" in content, "Script must execute ./auth_server"
    assert "--dev /dev" in content, "Script must bind mount /dev"
    assert "--proc /proc" in content, "Script must bind mount /proc"