# test_final_state.py
import os
import subprocess
import tempfile
import stat

def test_source_code_exists_and_contains_seccomp():
    source_path = "/home/user/secure_reader.c"
    assert os.path.exists(source_path), f"Source file {source_path} does not exist."
    with open(source_path, "r") as f:
        content = f.read()
    assert "PR_SET_SECCOMP" in content, "PR_SET_SECCOMP not found in source code."

def test_executable_exists():
    exe_path = "/home/user/secure_reader"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_auth_token_validation():
    exe_path = "/home/user/secure_reader"
    # Missing token
    env = os.environ.copy()
    if "AUTH_TOKEN" in env:
        del env["AUTH_TOKEN"]

    result = subprocess.run([exe_path, "/home/user/data/dummy"], env=env, capture_output=True)
    assert result.returncode == 1, f"Expected exit code 1 for missing token, got {result.returncode}"

    # Wrong token
    env["AUTH_TOKEN"] = "WRONG_TOKEN"
    result = subprocess.run([exe_path, "/home/user/data/dummy"], env=env, capture_output=True)
    assert result.returncode == 1, f"Expected exit code 1 for wrong token, got {result.returncode}"

def test_path_enforcement():
    exe_path = "/home/user/secure_reader"
    env = os.environ.copy()
    env["AUTH_TOKEN"] = "AUDITOR_TOKEN_99"

    # Bad prefix
    result = subprocess.run([exe_path, "/etc/passwd"], env=env, capture_output=True)
    assert result.returncode == 2, f"Expected exit code 2 for bad prefix, got {result.returncode}"

    # Directory traversal
    result = subprocess.run([exe_path, "/home/user/data/../data/dummy"], env=env, capture_output=True)
    assert result.returncode == 2, f"Expected exit code 2 for directory traversal, got {result.returncode}"

def test_file_preparation():
    exe_path = "/home/user/secure_reader"
    env = os.environ.copy()
    env["AUTH_TOKEN"] = "AUDITOR_TOKEN_99"

    # Missing file
    result = subprocess.run([exe_path, "/home/user/data/does_not_exist_12345.txt"], env=env, capture_output=True)
    assert result.returncode == 3, f"Expected exit code 3 for missing file, got {result.returncode}"

def test_valid_execution_and_encryption():
    exe_path = "/home/user/secure_reader"
    env = os.environ.copy()
    env["AUTH_TOKEN"] = "AUDITOR_TOKEN_99"

    os.makedirs("/home/user/data", exist_ok=True)
    test_file = "/home/user/data/test_audit.log"
    plaintext = b"SECURE_LOG_DATA_98765"
    with open(test_file, "wb") as f:
        f.write(plaintext)

    result = subprocess.run([exe_path, test_file], env=env, capture_output=True)
    assert result.returncode == 0, f"Expected exit code 0 for valid execution, got {result.returncode}"

    expected_output = bytes([b ^ 0x5A for b in plaintext])
    assert result.stdout == expected_output, "Output data does not match expected XORed output."

    # Cleanup
    os.remove(test_file)