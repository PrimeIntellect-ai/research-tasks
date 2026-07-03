# test_final_state.py

import os
import stat
import pytest

def test_task1_audit_ports():
    script_path = '/home/user/audit_ports.sh'
    log_path = '/home/user/active_ports.log'

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert '8065' in content, f"Expected port 8065 in {log_path}, but found: {content}"

def test_task2_file_integrity():
    log_path = '/home/user/modified_files.txt'

    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert 'app/public/app.js' in content or '/home/user/app/public/app.js' in content, \
        f"Expected modified file path (app.js) in {log_path}, but found: {content}"

def test_task3_auth_flow():
    script_path = '/home/user/test_auth.sh'
    log_path = '/home/user/auth_status.txt'

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert '200' == content, f"Expected HTTP status 200 in {log_path}, but found: {content}"

def test_task4_network_policy():
    script_path = '/home/user/block_ip.sh'
    acl_path = '/home/user/app/acl.conf'

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(acl_path), f"ACL file {acl_path} does not exist."

    with open(acl_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, f"ACL file {acl_path} is empty."
    assert lines[-1].strip() == 'deny 10.10.50.15', \
        f"Expected the last line of {acl_path} to be 'deny 10.10.50.15', but found: '{lines[-1]}'"

    st = os.stat(acl_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o444, \
        f"Expected permissions 444 for {acl_path}, but found {oct(permissions)}"