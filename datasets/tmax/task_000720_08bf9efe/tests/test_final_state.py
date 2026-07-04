# test_final_state.py

import os
import pytest
import stat

WORKSPACE_DIR = "/home/user/workspace"
VNC_MANAGER_FILE = os.path.join(WORKSPACE_DIR, "vnc_manager.go")
DEPLOY_SCRIPT = os.path.join(WORKSPACE_DIR, "deploy.sh")
DIAGNOSE_FILE = os.path.join(WORKSPACE_DIR, "diagnose.go")
AUDIT_LOG = os.path.join(WORKSPACE_DIR, "audit.log")

def test_vnc_manager_patched():
    """Test that vnc_manager.go has been patched to return 403."""
    assert os.path.isfile(VNC_MANAGER_FILE), f"File {VNC_MANAGER_FILE} does not exist."
    with open(VNC_MANAGER_FILE, 'r') as f:
        content = f.read()

    assert "Hardening check failed" in content, "The expected error message 'Hardening check failed' is missing from vnc_manager.go"

    # Check for 403 or http.StatusForbidden
    has_403 = "403" in content or "http.StatusForbidden" in content
    assert has_403, "The Go code must return a 403 status code (either as 403 or http.StatusForbidden)."

def test_deploy_script_exists_and_executable():
    """Test that deploy.sh exists, is executable, and configures the environment correctly."""
    assert os.path.isfile(DEPLOY_SCRIPT), f"File {DEPLOY_SCRIPT} does not exist."

    # Check if executable
    st = os.stat(DEPLOY_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{DEPLOY_SCRIPT} is not executable."

    with open(DEPLOY_SCRIPT, 'r') as f:
        content = f.read()

    assert "TZ=Asia/Tokyo" in content or 'export TZ="Asia/Tokyo"' in content or "export TZ=Asia/Tokyo" in content, "deploy.sh does not correctly set TZ=Asia/Tokyo"
    assert "VNC_PORT=8080" in content or 'export VNC_PORT="8080"' in content or "export VNC_PORT=8080" in content, "deploy.sh does not correctly set VNC_PORT=8080"
    assert "vnc_manager.go" in content, "deploy.sh does not seem to compile vnc_manager.go"

def test_diagnose_script_exists():
    """Test that diagnose.go exists."""
    assert os.path.isfile(DIAGNOSE_FILE), f"File {DIAGNOSE_FILE} does not exist."

def test_audit_log_content():
    """Test that audit.log exists and contains the correct result."""
    assert os.path.isfile(AUDIT_LOG), f"File {AUDIT_LOG} does not exist. Did the diagnostic tool run successfully?"

    with open(AUDIT_LOG, 'r') as f:
        content = f.read().strip()

    expected_content = "Result: 403 - Hardening check failed"
    # Sometime http.Error adds a newline, so we check if the expected text is in the content
    assert content.startswith("Result: 403 - Hardening check failed"), f"audit.log content is incorrect. Expected to start with '{expected_content}', got '{content}'"