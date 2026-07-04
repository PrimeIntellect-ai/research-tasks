# test_final_state.py

import os
import re
import hashlib
import stat

def get_expected_token():
    vuln_script_path = "/home/user/vuln_loop.sh"
    assert os.path.exists(vuln_script_path), f"Expected setup file {vuln_script_path} is missing."
    with open(vuln_script_path, "r") as f:
        content = f.read()

    match = re.search(r'/home/user/auth_tool\s+(\S+)', content)
    assert match is not None, "Could not extract token from vuln_loop.sh."
    return match.group(1)

def test_token_hash_file():
    hash_file_path = "/home/user/token_hash.txt"
    assert os.path.exists(hash_file_path), f"File {hash_file_path} does not exist."

    token = get_expected_token()
    expected_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()

    with open(hash_file_path, "r") as f:
        actual_content = f.read().strip()

    # Sometimes students might leave the filename in the output if they use `sha256sum` directly
    actual_hash = actual_content.split()[0]

    assert actual_hash == expected_hash, f"Hash in {hash_file_path} is incorrect. Expected {expected_hash}, got {actual_hash}."

def test_secure_invoke_script_exists_and_executable():
    script_path = "/home/user/secure_invoke.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

def test_secure_invoke_script_logic():
    script_path = "/home/user/secure_invoke.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "SECRET_TOKEN" in content, "The script does not seem to use the SECRET_TOKEN environment variable."
    assert "token.txt" in content, "The script does not seem to read from /home/user/token.txt."

    # Check that auth_tool is not being passed arguments directly like $1, $TOKEN, etc.
    # A simple heuristic: find the invocation of auth_tool and ensure it's not followed by a variable
    lines = content.splitlines()
    for line in lines:
        if "auth_tool" in line and not line.strip().startswith("#"):
            # If there's a $ after auth_tool, it's likely passing an argument
            match = re.search(r'auth_tool\s+.*\$', line)
            assert not match, "The script appears to pass arguments to auth_tool on the command line, which is insecure."