# test_final_state.py
import os
import stat
import subprocess
import pytest

PROJECT_DIR = "/home/user/provision_project"
DEPLOY_LOG = os.path.join(PROJECT_DIR, "deploy_status.log")
PROD_DAEMON = os.path.join(PROJECT_DIR, "production/daemon")
SUPERVISOR_SCRIPT = os.path.join(PROJECT_DIR, "supervisor.sh")

def test_deploy_status_log():
    assert os.path.exists(DEPLOY_LOG), f"{DEPLOY_LOG} was not created."
    with open(DEPLOY_LOG, 'r') as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"{DEPLOY_LOG} does not contain 'SUCCESS', got '{content}'"

def test_production_daemon_permissions():
    assert os.path.exists(PROD_DAEMON), f"Production binary not found at {PROD_DAEMON}."
    st = os.stat(PROD_DAEMON)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o500, f"Permissions on production daemon are not 500, got {oct(mode)}"

def test_daemon_behavior_wrong_key():
    assert os.path.exists(PROD_DAEMON), f"Production binary not found at {PROD_DAEMON}."
    proc = subprocess.run([PROD_DAEMON], input=b"WRONG\n", capture_output=True)
    assert proc.returncode == 1, f"Daemon did not exit with code 1 on wrong input, got {proc.returncode}"
    assert b"AUTH FAIL" in proc.stdout, "Daemon did not print AUTH FAIL on wrong input"

def test_daemon_behavior_correct_key():
    assert os.path.exists(PROD_DAEMON), f"Production binary not found at {PROD_DAEMON}."
    proc = subprocess.run([PROD_DAEMON], input=b"PROV-SEC-99\n", capture_output=True)
    assert proc.returncode == 0, f"Daemon did not exit with code 0 on correct input, got {proc.returncode}"
    assert b"INIT OK" in proc.stdout, "Daemon did not print INIT OK on correct input"

def test_supervisor_success_behavior(tmp_path):
    assert os.path.exists(SUPERVISOR_SCRIPT), f"{SUPERVISOR_SCRIPT} not found."

    dummy_succ = tmp_path / "dummy_succ.sh"
    dummy_succ.write_text("#!/bin/bash\nexit 0\n")
    dummy_succ.chmod(0o700)

    proc = subprocess.run([SUPERVISOR_SCRIPT, str(dummy_succ)], capture_output=True)
    assert b"STOPPING" in proc.stdout, "Supervisor did not print STOPPING on successful execution of the child process"

def test_supervisor_restarting_logic():
    assert os.path.exists(SUPERVISOR_SCRIPT), f"{SUPERVISOR_SCRIPT} not found."
    with open(SUPERVISOR_SCRIPT, 'r') as f:
        content = f.read()
    assert "RESTARTING" in content, "Supervisor script does not contain RESTARTING logic"