# test_final_state.py

import os
import re
import pytest

def get_expected_flag():
    """Extract the expected flag directly from the backend source code."""
    backend_path = '/home/user/backend/server.js'
    if not os.path.isfile(backend_path):
        return "FLAG{jwt_evasion_master_9921}" # Fallback if file is missing

    with open(backend_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'const\s+FLAG\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return "FLAG{jwt_evasion_master_9921}"

def test_flag_file_exists_and_correct():
    flag_path = '/home/user/flag.txt'
    assert os.path.isfile(flag_path), f"The flag file was not found at {flag_path}. Ensure you have saved the flag."

    with open(flag_path, 'r', encoding='utf-8') as f:
        actual_flag = f.read().strip()

    expected_flag = get_expected_flag()

    assert actual_flag == expected_flag, f"The flag found in {flag_path} is incorrect. Expected the secret flag from the backend."