# test_final_state.py

import os
import stat
import ast

def test_recovered_token():
    """Check that the token was successfully recovered via the vulnerability scan."""
    path = "/home/user/recovered_token.txt"
    assert os.path.isfile(path), f"File {path} is missing. The scanner script may not have saved the output correctly."

    with open(path, "r") as f:
        content = f.read()

    expected = "FLAG{traversal_identified_992}"
    assert content == expected, f"Content of {path} is incorrect. Expected '{expected}', got '{content}'."

def test_target_rsa_permissions():
    """Check that the exposed RSA key permissions were properly hardened."""
    path = "/home/user/target_rsa"
    assert os.path.isfile(path), f"File {path} is missing."

    st = os.stat(path)
    perms = oct(st.st_mode)[-3:]
    assert perms == "600", f"Permissions of {path} are insecure. Expected 600, got {perms}."

def test_ssh_config_harden():
    """Check that the SSH config snippet is correctly configured."""
    path = "/home/user/ssh_config_harden"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = f.readlines()

    in_target_server = False
    has_identity_file = False
    has_password_auth = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Handle both space and equals sign separators
        if "=" in line:
            key, val = [x.strip() for x in line.split("=", 1)]
        else:
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            key, val = parts

        key_lower = key.lower()

        if key_lower == "host":
            if val == "target-server":
                in_target_server = True
            else:
                in_target_server = False
        elif in_target_server:
            if key_lower == "identityfile" and val == "/home/user/target_rsa":
                has_identity_file = True
            elif key_lower == "passwordauthentication" and val.lower() == "no":
                has_password_auth = True

    assert has_identity_file, "IdentityFile is not correctly set to /home/user/target_rsa for host target-server."
    assert has_password_auth, "PasswordAuthentication is not explicitly disabled (set to 'no') for host target-server."

def test_scanner_script_validity():
    """Check that the scanner script exists and contains valid Python syntax."""
    path = "/home/user/scanner.py"
    assert os.path.isfile(path), f"File {path} is missing. Did you write the scanner script?"

    with open(path, "r") as f:
        content = f.read()

    try:
        ast.parse(content)
    except SyntaxError as e:
        assert False, f"The script {path} contains invalid Python syntax: {e}"