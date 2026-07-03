# test_final_state.py
import os
import re

def test_exploit_results_file():
    """Verify that the exploit script successfully ran against the vulnerable server."""
    file_path = "/home/user/exploit_results.txt"
    assert os.path.isfile(file_path), f"Expected result file {file_path} does not exist. Did the exploit script run?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "VULNERABLE: OPEN_REDIRECT, XSS, FORGED_TOKEN"
    assert expected_content in content, (
        f"File {file_path} does not contain the expected success string. "
        f"Expected '{expected_content}', but got '{content}'."
    )

def test_fixed_results_file():
    """Verify that the exploit script failed against the patched server."""
    file_path = "/home/user/fixed_results.txt"
    assert os.path.isfile(file_path), f"Expected result file {file_path} does not exist. Did the script run against the patched server?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "SECURE: EXPLOITS_FAILED"
    assert expected_content in content, (
        f"File {file_path} does not contain the expected success string. "
        f"Expected '{expected_content}', but got '{content}'."
    )

def test_patch_urandom_used():
    """Verify the C server was patched to use /dev/urandom for token generation."""
    file_path = "/home/user/auth_server.c"
    assert os.path.isfile(file_path), f"Source file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "/dev/urandom" in content, (
        "The patched server does not appear to read from '/dev/urandom'. "
        "Token generation must be secured using a cryptographically secure pseudorandom number generator."
    )

def test_patch_open_redirect_fixed():
    """Verify the C server was patched to validate redirect URLs."""
    file_path = "/home/user/auth_server.c"
    with open(file_path, "r") as f:
        content = f.read()

    # Look for logic that checks if the redirect starts with '/' and handles it
    # We'll check for the presence of a character check against '/'
    has_slash_check = re.search(r"redirect_url\[0\]\s*==\s*'\/'", content) or re.search(r"redirect_url\[0\]\s*!=\s*'\/'", content)
    # Also look for double slash check to prevent protocol relative URLs like //malicious.com
    has_double_slash_check = re.search(r"redirect_url\[1\]\s*==\s*'\/'", content) or strstr_check in content
    strstr_check = "strstr" in content and "//" in content

    # A more generic check: look for any validation logic applied to redirect_url before use
    validation_present = has_slash_check or ("/" in content and "redirect_url" in content and ("if" in content or "?" in content))

    assert validation_present, (
        "Could not detect open redirect validation in auth_server.c. "
        "Ensure the code checks that the redirect URL starts with a single '/'."
    )

def test_patch_xss_fixed():
    """Verify the C server was patched to HTML-encode user input to prevent XSS."""
    file_path = "/home/user/auth_server.c"
    with open(file_path, "r") as f:
        content = f.read()

    # Check for HTML entity encoding strings
    has_lt = "&lt;" in content
    has_gt = "&gt;" in content

    assert has_lt and has_gt, (
        "Could not detect HTML entity encoding ('&lt;' and '&gt;') in auth_server.c. "
        "The username must be sanitized before being echoed in the HTTP response."
    )