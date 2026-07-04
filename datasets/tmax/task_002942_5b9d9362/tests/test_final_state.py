# test_final_state.py

import os
import stat
import subprocess
import pytest
import re

SCRIPT_PATH = '/home/user/process_intercepts.sh'
INTERCEPTS_DIR = '/home/user/intercepts'
REDACTED_DIR = '/home/user/vuln_redacted'

def test_script_exists_and_executable():
    """Test that the script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_uses_unshare():
    """Test that the script uses unshare -n openssl."""
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # We look for unshare -n and openssl. They might be separated by spaces or quotes.
    assert re.search(r'unshare\s+-n\s+openssl', content), "Script does not appear to use 'unshare -n openssl' for network isolation."

def test_script_execution_and_output_files():
    """Run the script and verify it populates the correct files."""
    # Clean the redacted directory in case it has old artifacts
    for f in os.listdir(REDACTED_DIR):
        os.remove(os.path.join(REDACTED_DIR, f))

    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    expected_files = {'cert2.pem', 'cert4.pem'}
    actual_files = set(os.listdir(REDACTED_DIR))

    assert actual_files == expected_files, f"Expected {expected_files} in {REDACTED_DIR}, but got {actual_files}."

def test_redaction_format():
    """Test that the private keys are properly redacted."""
    # Ensure the script has been run and files are present
    expected_files = ['cert2.pem', 'cert4.pem']
    for filename in expected_files:
        filepath = os.path.join(REDACTED_DIR, filename)
        assert os.path.isfile(filepath), f"{filepath} is missing."

        with open(filepath, 'r') as f:
            content = f.read()

        # Check that the certificate part is still there
        assert '-----BEGIN CERTIFICATE-----' in content, f"Certificate block missing in {filename}."
        assert '-----END CERTIFICATE-----' in content, f"Certificate end block missing in {filename}."

        # Check that the private key block is redacted
        # It could be BEGIN PRIVATE KEY or BEGIN RSA PRIVATE KEY
        match = re.search(r'(-----BEGIN (?:RSA )?PRIVATE KEY-----)\n(.*?)\n(-----END (?:RSA )?PRIVATE KEY-----)', content, re.DOTALL)
        assert match is not None, f"Private key block missing or malformed in {filename}."

        key_body = match.group(2).strip()
        assert key_body == '[REDACTED]', f"Private key material was not properly redacted in {filename}. Found: {key_body}"