# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
TOKEN_GEN_CPP = os.path.join(WORKSPACE_DIR, "token_gen.cpp")
NEW_TOKEN_TXT = os.path.join(WORKSPACE_DIR, "new_token.txt")
VERIFY_SH = os.path.join(WORKSPACE_DIR, "verify.sh")

def test_token_gen_cpp_exists():
    """Test that the token_gen.cpp source file exists."""
    assert os.path.isfile(TOKEN_GEN_CPP), f"File {TOKEN_GEN_CPP} is missing."

def test_new_token_txt_content():
    """Test that new_token.txt contains the correctly computed hex string."""
    assert os.path.isfile(NEW_TOKEN_TXT), f"File {NEW_TOKEN_TXT} is missing."
    with open(NEW_TOKEN_TXT, "r") as f:
        content = f.read().strip()

    # Compute the expected token dynamically based on the task description
    secret = "r0t4t10n_M4st3r_99"
    date_str = "20241231"
    expected_hex = ""
    for i, char in enumerate(secret):
        date_char = date_str[i % len(date_str)]
        xor_val = ord(char) ^ ord(date_char)
        expected_hex += f"{xor_val:02x}"

    assert content == expected_hex, f"Content of {NEW_TOKEN_TXT} is incorrect. Expected '{expected_hex}', got '{content}'."

def test_verify_sh_exists_and_executable():
    """Test that verify.sh exists and is executable."""
    assert os.path.isfile(VERIFY_SH), f"File {VERIFY_SH} is missing."
    assert os.access(VERIFY_SH, os.X_OK), f"File {VERIFY_SH} is not executable."

def test_verify_sh_contents():
    """Test that verify.sh contains the required unshare flags and executes the binary."""
    with open(VERIFY_SH, "r") as f:
        content = f.read()
    assert "unshare" in content, f"{VERIFY_SH} does not use the 'unshare' utility."
    assert "--net" in content, f"{VERIFY_SH} does not use the '--net' flag for network namespace isolation."
    assert "--ipc" in content, f"{VERIFY_SH} does not use the '--ipc' flag for IPC namespace isolation."
    assert "auth_service" in content, f"{VERIFY_SH} does not appear to execute the 'auth_service' binary."

def test_verify_sh_execution():
    """Test that running verify.sh succeeds (returns exit code 0)."""
    # Execute verify.sh from the workspace directory since it might use relative paths
    result = subprocess.run([VERIFY_SH], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {VERIFY_SH} failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"