# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

AUDIT_TRAIL_PATH = "/home/user/audit_trail.json"
SERVER_GO_PATH = "/home/user/app/server.go"
SERVER_BIN_PATH = "/home/user/app/server"
SANDBOX_SH_PATH = "/home/user/sandbox.sh"

def test_audit_trail_json():
    assert os.path.exists(AUDIT_TRAIL_PATH), f"{AUDIT_TRAIL_PATH} does not exist."
    with open(AUDIT_TRAIL_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{AUDIT_TRAIL_PATH} is not valid JSON.")

    assert data.get("listening_port") == 8443, "listening_port in audit_trail.json is incorrect."
    assert data.get("vulnerability_cwe") == "CWE-330", "vulnerability_cwe in audit_trail.json is incorrect."
    assert data.get("remediation_action") == "Applied CSP and Sandboxing", "remediation_action in audit_trail.json is incorrect."

def test_server_go_csp_header():
    assert os.path.exists(SERVER_GO_PATH), f"{SERVER_GO_PATH} does not exist."
    with open(SERVER_GO_PATH, "r") as f:
        content = f.read()

    expected_csp = "Content-Security-Policy"
    expected_value1 = "default-src 'self'"
    expected_value2 = "script-src 'none'"
    expected_value3 = "object-src 'none'"

    assert expected_csp in content, "CSP header name not found in server.go"
    assert expected_value1 in content, "CSP header default-src directive missing or incorrect"
    assert expected_value2 in content, "CSP header script-src directive missing or incorrect"
    assert expected_value3 in content, "CSP header object-src directive missing or incorrect"

def test_server_binary_compiled():
    assert os.path.exists(SERVER_BIN_PATH), f"{SERVER_BIN_PATH} does not exist. Did you compile the Go server?"
    assert os.access(SERVER_BIN_PATH, os.X_OK), f"{SERVER_BIN_PATH} is not executable."

def test_sandbox_sh():
    assert os.path.exists(SANDBOX_SH_PATH), f"{SANDBOX_SH_PATH} does not exist."

    st = os.stat(SANDBOX_SH_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SANDBOX_SH_PATH} is not executable."

    with open(SANDBOX_SH_PATH, "r") as f:
        content = f.read()

    assert "bwrap" in content, "bwrap command not found in sandbox.sh"
    assert "--ro-bind / /" in content or ("--ro-bind" in content and "/" in content), "--ro-bind / / missing in sandbox.sh"
    assert "--bind /home/user/app /home/user/app" in content or ("--bind" in content and "/home/user/app" in content), "--bind /home/user/app /home/user/app missing in sandbox.sh"
    assert "--unshare-net" in content, "--unshare-net missing in sandbox.sh"

    # Check directory change
    has_chdir_arg = "--chdir /home/user/app" in content
    has_cd_cmd = "cd /home/user/app" in content
    assert has_chdir_arg or has_cd_cmd, "Must change directory to /home/user/app before or during bwrap execution."

    assert "./server" in content or "/home/user/app/server" in content, "Must execute the server binary in the bwrap command."