# test_final_state.py

import os
import zipfile
import pytest

def test_backup_created():
    backup_path = "/home/user/mail/backup/backup_current.zip"
    assert os.path.isfile(backup_path), f"Backup zip file missing at {backup_path}"

    with zipfile.ZipFile(backup_path, 'r') as z:
        namelist = [os.path.basename(name) for name in z.namelist()]
        assert "msg1.eml" in namelist, "msg1.eml not found in the backup zip"
        assert "msg2.eml" in namelist, "msg2.eml not found in the backup zip"

def test_processed_msg1():
    msg1_path = "/home/user/mail/processed/msg1.eml"
    assert os.path.isfile(msg1_path), f"Processed msg1.eml missing at {msg1_path}"

    with open(msg1_path, 'r') as f:
        content = f.read()

    assert "X-Internal-Route:" not in content, "X-Internal-Route header was not removed from msg1.eml"
    assert content.strip().endswith("Status: Processed"), "msg1.eml does not end with 'Status: Processed'"

def test_processed_msg2():
    msg2_path = "/home/user/mail/processed/msg2.eml"
    assert os.path.isfile(msg2_path), f"Processed msg2.eml missing at {msg2_path}"

    with open(msg2_path, 'r') as f:
        content = f.read()

    assert "X-Internal-Route:" not in content, "X-Internal-Route header was not removed from msg2.eml"
    assert "X-Safe-Header: true" in content, "X-Safe-Header was incorrectly removed from msg2.eml"
    assert content.strip().endswith("Status: Processed"), "msg2.eml does not end with 'Status: Processed'"

def test_symlink_created():
    symlink_path = "/home/user/current_processor.py"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"

    target = os.readlink(symlink_path)
    assert os.path.basename(target) == "processor_v2.py" or target == "/home/user/processor_v2.py", \
        f"Symlink points to {target} instead of processor_v2.py"

def test_deployment_success_log():
    log_path = "/home/user/deploy_success.log"
    assert os.path.isfile(log_path), f"Deployment success log missing at {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "DEPLOYMENT COMPLETE" in content, "deploy_success.log does not contain 'DEPLOYMENT COMPLETE'"

def test_supervisord_running():
    pid_path = "/home/user/supervisord.pid"
    assert os.path.isfile(pid_path), f"Supervisord pid file missing at {pid_path}. Is supervisord running?"