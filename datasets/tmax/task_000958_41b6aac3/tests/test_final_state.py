# test_final_state.py

import os
import subprocess
import random
import pytest

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/app/nginx/nginx.conf"
    assert os.path.exists(nginx_conf_path), f"Nginx config missing at {nginx_conf_path}"
    with open(nginx_conf_path, "r") as f:
        content = f.read()
    assert "wrong.sock" not in content, "Nginx config still points to 'wrong.sock'"
    assert "/home/user/app/private/api.sock" in content, "Nginx config does not point to the correct api.sock path"

def test_acls_configured():
    private_dir = "/home/user/app/private"
    api_sock = "/home/user/app/private/api.sock"

    # Check directory ACL
    assert os.path.exists(private_dir), f"Directory {private_dir} missing"
    res_dir = subprocess.run(["getfacl", private_dir], capture_output=True, text=True)
    assert res_dir.returncode == 0, "Failed to run getfacl on private directory"

    # We expect user:guest:--x or user:guest:r-x or user:guest:rwx
    # Just look for user:guest: and check if 'x' is in the permissions part
    guest_dir_acl = [line for line in res_dir.stdout.splitlines() if line.startswith("user:guest:")]
    assert guest_dir_acl, "No ACL entry found for user 'guest' on private directory"
    perms = guest_dir_acl[0].split(":")[2]
    assert "x" in perms, f"Guest user does not have execute permission on {private_dir}, got: {perms}"

    # Check socket ACL
    assert os.path.exists(api_sock), f"Socket file {api_sock} missing"
    res_sock = subprocess.run(["getfacl", api_sock], capture_output=True, text=True)
    assert res_sock.returncode == 0, "Failed to run getfacl on api.sock"

    guest_sock_acl = [line for line in res_sock.stdout.splitlines() if line.startswith("user:guest:")]
    assert guest_sock_acl, "No ACL entry found for user 'guest' on api.sock"
    perms = guest_sock_acl[0].split(":")[2]
    assert "r" in perms and "w" in perms, f"Guest user does not have rw permissions on {api_sock}, got: {perms}"

def test_sanitize_subject_fuzz_equivalence():
    oracle_path = "/home/user/app/oracle_sanitize"
    agent_path = "/home/user/app/sanitize_subject"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent program missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable"

    random.seed(42)
    N = 1000

    for i in range(N):
        length = random.randint(1, 2048)
        input_bytes = bytes(random.choices(range(256), k=length))

        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_bytes,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, "Oracle failed to execute"

        agent_proc = subprocess.run(
            [agent_path],
            input=input_bytes,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent program failed (exit code {agent_proc.returncode}) on input length {length}"

        if oracle_proc.stdout != agent_proc.stdout:
            # Truncate for display if too long
            disp_input = input_bytes[:100] + b"..." if len(input_bytes) > 100 else input_bytes
            disp_oracle = oracle_proc.stdout[:100] + b"..." if len(oracle_proc.stdout) > 100 else oracle_proc.stdout
            disp_agent = agent_proc.stdout[:100] + b"..." if len(agent_proc.stdout) > 100 else agent_proc.stdout

            pytest.fail(
                f"Mismatch found on random input!\n"
                f"Input (hex): {disp_input.hex()}\n"
                f"Oracle output: {disp_oracle}\n"
                f"Agent output: {disp_agent}"
            )