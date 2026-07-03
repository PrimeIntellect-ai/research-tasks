# test_final_state.py

import os
import subprocess
import pytest

def test_domains_txt_content():
    domains_file = '/home/user/forensics/domains.txt'
    assert os.path.isfile(domains_file), f"File {domains_file} does not exist."

    with open(domains_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_domains = ['attacker.net', 'badguy.io', 'malicious-phish.com']
    assert lines == expected_domains, f"Content of {domains_file} is incorrect. Expected {expected_domains}, got {lines}."

def test_clean_authorized_keys_content():
    original_keys_file = '/home/user/.ssh/authorized_keys'
    clean_keys_file = '/home/user/forensics/clean_authorized_keys'

    assert os.path.isfile(original_keys_file), f"Original file {original_keys_file} is missing."
    assert os.path.isfile(clean_keys_file), f"Cleaned file {clean_keys_file} does not exist."

    with open(original_keys_file, 'r') as f:
        original_lines = f.readlines()

    expected_line = next((line for line in original_lines if 'analyst@soc.local' in line), None)
    assert expected_line is not None, "Could not find the valid key in the original authorized_keys file."

    with open(clean_keys_file, 'r') as f:
        clean_content = f.read()

    assert clean_content == expected_line, f"Content of {clean_keys_file} is incorrect. It should contain exactly the valid key with no extra blank lines."

def test_test_security_py():
    test_file = '/home/user/app/test_security.py'
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    with open(test_file, 'r') as f:
        content = f.read()

    assert 'unittest' in content, f"{test_file} does not appear to use the unittest framework."
    assert 'Content-Security-Policy' in content, f"{test_file} does not check for the Content-Security-Policy header."
    assert "default-src 'self'; script-src 'self'" in content, f"{test_file} does not check for the exact CSP value."
    assert 'from app import app' in content or 'import app' in content, f"{test_file} does not import the Flask app."

    # Run the unit test
    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/user/app'
    result = subprocess.run(
        ['python3', '-m', 'unittest', test_file],
        capture_output=True,
        text=True,
        env=env
    )

    assert result.returncode == 0, f"The unit test {test_file} failed when executed:\n{result.stderr}\n{result.stdout}"