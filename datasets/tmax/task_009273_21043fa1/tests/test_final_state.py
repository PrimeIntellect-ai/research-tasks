# test_final_state.py

import os
import json
import hashlib

def test_audit_trail_json_exists_and_valid():
    """Test if /home/user/audit_trail.json exists and contains the correct data."""
    audit_file = '/home/user/audit_trail.json'
    assert os.path.isfile(audit_file), f"{audit_file} does not exist."

    with open(audit_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{audit_file} does not contain valid JSON."

    assert 'httponly_flag_present' in data, "Key 'httponly_flag_present' missing in JSON."
    assert data['httponly_flag_present'] is False, "Expected 'httponly_flag_present' to be false."

    expected_hash = hashlib.sha256(b'COMPLIANCE_CONFIDENTIAL_DATA_9921').hexdigest()
    assert 'file_sha256' in data, "Key 'file_sha256' missing in JSON."
    assert data['file_sha256'] == expected_hash, f"Expected 'file_sha256' to be {expected_hash}, got {data['file_sha256']}."

def test_run_isolated_sh_exists_and_correct():
    """Test if /home/user/run_isolated.sh exists and contains the required bwrap command."""
    script_file = '/home/user/run_isolated.sh'
    assert os.path.isfile(script_file), f"{script_file} does not exist."

    with open(script_file, 'r') as f:
        content = f.read()

    assert 'bwrap' in content, "bwrap command not found in the script."
    assert '--ro-bind / /' in content, "--ro-bind / / not found in the script."
    assert '--bind /home/user/audit_trail.json /home/user/audit_trail.json' in content, "--bind for audit_trail.json not found in the script."
    assert '--share-net' in content, "--share-net not found in the script."
    assert '/usr/bin/python3 /home/user/audit.py' in content, "Command to run python script not found in the script."