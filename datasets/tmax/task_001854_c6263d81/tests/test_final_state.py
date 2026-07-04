# test_final_state.py

import os
import subprocess
import re

def test_redacted_requests_log():
    original_log = '/home/user/auth_requests.log'
    redacted_log = '/home/user/redacted_requests.log'

    assert os.path.isfile(original_log), f"Original log file {original_log} is missing."
    assert os.path.isfile(redacted_log), f"Redacted log file {redacted_log} is missing."

    with open(original_log, 'r') as f:
        original_lines = f.read().splitlines()

    with open(redacted_log, 'r') as f:
        redacted_lines = f.read().splitlines()

    assert len(original_lines) == len(redacted_lines), "Redacted log does not have the same number of lines as the original log."

    # Check that original passwords are gone and replaced by [REDACTED]
    for orig, red in zip(original_lines, redacted_lines):
        # Extract the original password
        match = re.search(r'pwd=([^&\s]+)', orig)
        if match:
            orig_pwd = match.group(1)
            assert orig_pwd not in red, f"Original password '{orig_pwd}' was not redacted in line: {red}"

        assert "pwd=[REDACTED]" in red, f"Expected 'pwd=[REDACTED]' not found in line: {red}"

        # Strip out the pwd parameter to ensure the rest of the line is intact
        orig_stripped = re.sub(r'pwd=[^&\s]+', '', orig)
        red_stripped = re.sub(r'pwd=\[REDACTED\]', '', red)
        assert orig_stripped == red_stripped, f"Other parts of the line were modified. Original (stripped): {orig_stripped}, Redacted (stripped): {red_stripped}"

def test_compilation():
    binary_path = '/home/user/auth_cgi'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_command_injection_fix():
    binary_path = '/home/user/auth_cgi'
    access_log = '/home/user/access.log'
    hacked_file = '/tmp/hacked'

    if os.path.exists(access_log):
        os.remove(access_log)
    if os.path.exists(hacked_file):
        os.remove(hacked_file)

    env = os.environ.copy()
    env['QUERY_STRING'] = "user=hacker;touch /tmp/hacked&redirect=https://evil.com"

    subprocess.run([binary_path], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert not os.path.exists(hacked_file), "Command injection vulnerability still exists: /tmp/hacked was created."

    assert os.path.isfile(access_log), f"Access log {access_log} was not created."
    with open(access_log, 'r') as f:
        content = f.read()

    assert "Access by hacker;touch /tmp/hacked" in content, "Log entry does not contain the exact injected string, suggesting improper file I/O or truncation."

def test_open_redirect_fix():
    binary_path = '/home/user/auth_cgi'

    # Test 1: Malicious external redirect
    env = os.environ.copy()
    env['QUERY_STRING'] = "user=admin&redirect=https://evil.com"
    result1 = subprocess.run([binary_path], env=env, stdout=subprocess.PIPE, text=True)
    assert "Location: https://evil.com" not in result1.stdout, "Open redirect vulnerability still exists: Location header allowed 'https://evil.com'."

    # Test 2: Safe internal redirect
    env['QUERY_STRING'] = "user=admin&redirect=/safe"
    result2 = subprocess.run([binary_path], env=env, stdout=subprocess.PIPE, text=True)
    assert "Location: /safe" in result2.stdout, "Safe redirect to '/safe' was improperly blocked."

    # Test 3: Protocol-relative URL bypass
    env['QUERY_STRING'] = "user=admin&redirect=//evil.com"
    result3 = subprocess.run([binary_path], env=env, stdout=subprocess.PIPE, text=True)
    assert "Location: //evil.com" not in result3.stdout, "Open redirect vulnerability still exists: Location header allowed protocol-relative URL '//evil.com'."

def test_csp_header():
    binary_path = '/home/user/auth_cgi'

    env = os.environ.copy()
    env['QUERY_STRING'] = "user=admin&redirect=/safe"
    result = subprocess.run([binary_path], env=env, stdout=subprocess.PIPE, text=True)

    assert "Content-Security-Policy: default-src 'self';" in result.stdout, "Content-Security-Policy header is missing or incorrect."

    # Verify it appears before the blank line separating headers from body
    header_section = result.stdout.split('\n\n')[0]
    assert "Content-Security-Policy: default-src 'self';" in header_section, "Content-Security-Policy header must be in the HTTP headers section (before the blank line)."