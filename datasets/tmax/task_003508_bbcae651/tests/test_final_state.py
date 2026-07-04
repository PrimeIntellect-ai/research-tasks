# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy_update.sh"
    assert os.path.isfile(script_path), f"Deployment script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Deployment script is not executable: {script_path}"

def test_deployed_files_and_permissions():
    expected_files = {
        "api/server.py": {"perms": "750", "acl_user": "www-data", "acl_perms": "r-x"},
        "config/db.conf": {"perms": "600", "acl_user": "www-data", "acl_perms": "r--"},
        "static/style.css": {"perms": "644", "acl_user": "daemon", "acl_perms": "r--"}
    }

    prod_dir = "/home/user/production"
    for rel_path, expected in expected_files.items():
        full_path = os.path.join(prod_dir, rel_path)
        assert os.path.isfile(full_path), f"Deployed file missing: {full_path}"

        # Verify ACL and base permissions using getfacl
        result = subprocess.run(["getfacl", "-p", full_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to run getfacl on {full_path}"

        output = result.stdout
        acl_line = f"user:{expected['acl_user']}:{expected['acl_perms']}"
        assert acl_line in output, f"ACL rule '{acl_line}' not found in getfacl output for {full_path}:\n{output}"

def test_audit_log_content():
    log_path = "/home/user/audit.log"
    assert os.path.isfile(log_path), f"Audit log missing: {log_path}"

    expected_lines = [
        "FILE: api/server.py - PERMS: 750 - ACL: www-data:r-x",
        "FILE: config/db.conf - PERMS: 600 - ACL: www-data:r--",
        "FILE: static/style.css - PERMS: 644 - ACL: daemon:r--"
    ]

    with open(log_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == len(expected_lines), f"Audit log should have exactly {len(expected_lines)} lines, found {len(content)}."

    for expected in expected_lines:
        assert expected in content, f"Missing expected audit log line: '{expected}'"