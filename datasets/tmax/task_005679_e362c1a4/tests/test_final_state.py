# test_final_state.py

import os
import stat
import subprocess

def test_block_rules_sh():
    script_path = "/home/user/block_rules.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Check execution permissions
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} does not have execution permissions."

    with open(script_path, "r") as f:
        content = f.read().strip()

    # Ignore shebang if present
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    assert len(lines) == 1, f"{script_path} should contain exactly one iptables command."
    assert lines[0] == "iptables -A INPUT -s 198.51.100.42 -j DROP", f"{script_path} contains incorrect iptables command."

def test_audit_token_txt():
    token_path = "/home/user/audit_token.txt"
    assert os.path.isfile(token_path), f"{token_path} does not exist."

    with open(token_path, "r") as f:
        content = f.read().strip()

    assert content == "AUTH_SECRET_99", f"{token_path} does not contain the correct decrypted token."

def test_decrypt_sh():
    script_path = "/home/user/decrypt.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Test the script's functionality
    try:
        result = subprocess.run(
            ["bash", script_path, "7a6e6f7364687e78697e7f640202"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert "AUTH_SECRET_99" in result.stdout.strip(), f"{script_path} did not output the correct plaintext for the given ciphertext."
    except Exception as e:
        assert False, f"Failed to execute {script_path}: {e}"