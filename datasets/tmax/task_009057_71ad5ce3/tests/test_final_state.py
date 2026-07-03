# test_final_state.py

import os
import hashlib
import re
import stat

def test_compromised_ips_log_parsing():
    """Validates that the compromised IPs were correctly extracted and sorted."""
    output_file = "/home/user/compromised_ips.txt"
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # We derive the expected IPs based on the rules:
    # 1. /login endpoint
    # 2. next parameter starts with http:// or https://
    # 3. HTTP status 302
    expected_ips = ["10.0.0.5", "203.0.113.42"]

    assert lines == expected_ips, (
        f"The IPs in {output_file} are incorrect or not sorted properly. "
        f"Expected {expected_ips}, but got {lines}. "
        "Ensure you only matched absolute URLs (http:// or https://) with a 302 status."
    )

def test_go_code_credential_rotation():
    """Validates that the Go code uses SHA-256 for the new password and removes the plaintext."""
    go_file = "/home/user/app/auth_server.go"
    assert os.path.isfile(go_file), f"The source file {go_file} is missing."

    with open(go_file, "r") as f:
        content = f.read()

    # Recompute the expected hash
    new_password = "Str0ngR0tat1on!88"
    expected_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

    assert expected_hash in content, (
        f"The Go code does not contain the correct SHA-256 hash of the new password. "
        f"Expected to find hash: {expected_hash}"
    )
    assert new_password not in content, "The new password must not be stored in plaintext in the code."
    assert "supersecret_legacy" not in content, "The legacy plaintext password is still in the code."
    assert "crypto/sha256" in content, "The 'crypto/sha256' package is not imported in the Go code."

def test_go_code_open_redirect_fix():
    """Validates that the Go code includes logic to prevent open redirects."""
    go_file = "/home/user/app/auth_server.go"
    with open(go_file, "r") as f:
        content = f.read()

    # The code should check that 'next' starts with '/' but not '//'
    # We look for common string manipulation functions or literal checks
    has_slash_check = 'HasPrefix' in content or 'next[0]' in content or 'StartsWith' in content or '"/"' in content
    has_double_slash_check = '"//"' in content

    assert has_slash_check and has_double_slash_check, (
        "The Go code does not appear to properly validate the 'next' parameter for relative paths. "
        "Ensure you check that it starts with '/' and does NOT start with '//'."
    )
    assert "/dashboard" in content, "The fallback redirect to '/dashboard' is missing."

def test_run_isolated_script():
    """Validates the bash script for process isolation and compilation."""
    script_file = "/home/user/run_isolated.sh"
    assert os.path.isfile(script_file), f"The script {script_file} is missing."

    # Check if executable
    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_file} is not executable (chmod +x)."

    with open(script_file, "r") as f:
        content = f.read()

    # Check for compilation
    assert re.search(r'go\s+build', content), "The script does not contain a 'go build' command to compile the executable."
    assert "auth_server" in content, "The script does not reference the 'auth_server' executable."

    # Check for unshare with network namespace isolation
    unshare_match = re.search(r'unshare\s+(.*)', content)
    assert unshare_match, "The script does not use the 'unshare' command."

    unshare_args = unshare_match.group(1)
    assert "-n" in unshare_args.split() or "--net" in unshare_args.split(), (
        "The 'unshare' command does not include the flag for network namespace isolation (-n or --net)."
    )