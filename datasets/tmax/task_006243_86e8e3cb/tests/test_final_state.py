# test_final_state.py

import os
import stat
import json
import base64
import hashlib
import pytest

def decode_base64_url(s):
    # Add padding if necessary
    s = s + '=' * (-len(s) % 4)
    # Replace URL-safe chars
    s = s.replace('-', '+').replace('_', '/')
    return base64.b64decode(s).decode('utf-8')

def test_phase1_jwt_analysis():
    log_file = '/home/user/auth_logs.jsonl'
    output_file = '/home/user/compromised_subs.txt'

    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_subs = set()
    with open(log_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                token = data.get('token', '')
                parts = token.split('.')
                if len(parts) >= 2:
                    header = json.loads(decode_base64_url(parts[0]))
                    if header.get('alg', '').lower() == 'none':
                        payload = json.loads(decode_base64_url(parts[1]))
                        if 'sub' in payload:
                            expected_subs.add(payload['sub'])
            except Exception:
                continue

    expected_sorted = sorted(list(expected_subs))

    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert actual_lines == expected_sorted, f"Expected compromised subjects {expected_sorted}, but got {actual_lines}"

def test_phase2_ssh_key_audit():
    keys_dir = '/home/user/ssh_keys'
    output_file = '/home/user/weak_ssh_keys.txt'

    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_weak_keys = []
    if os.path.isdir(keys_dir):
        for filename in os.listdir(keys_dir):
            if filename.startswith('id_'):
                filepath = os.path.join(keys_dir, filename)
                if os.path.isfile(filepath):
                    st = os.stat(filepath)
                    perms = stat.S_IMODE(st.st_mode)
                    # Check if permissions are broader than 600 (i.e. group or others have any access)
                    if perms & 0o077 != 0:
                        expected_weak_keys.append(filepath)

    expected_sorted = sorted(expected_weak_keys)

    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert actual_lines == expected_sorted, f"Expected weak SSH keys {expected_sorted}, but got {actual_lines}"

def test_phase3_privesc_auditing():
    scripts_dir = '/home/user/scripts'
    output_file = '/home/user/privesc_vuln.txt'

    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_lines = []
    if os.path.isdir(scripts_dir):
        for filename in os.listdir(scripts_dir):
            filepath = os.path.join(scripts_dir, filename)
            if os.path.isfile(filepath):
                st = os.stat(filepath)
                # Check if world-writable
                if st.st_mode & stat.S_IWOTH:
                    hasher = hashlib.sha256()
                    with open(filepath, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hasher.update(chunk)
                    expected_lines.append(f"{hasher.hexdigest()}  {filepath}")

    # The expected output should match one of the world-writable files.
    # Since the setup creates exactly one, we expect exactly one line.
    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    # Standardize spaces for comparison
    actual_standardized = [" ".join(line.split()) for line in actual_lines]
    expected_standardized = [" ".join(line.split()) for line in expected_lines]

    assert actual_standardized == expected_standardized, f"Expected privesc output {expected_standardized}, but got {actual_standardized}"