# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_pre_receive_hook_fixed():
    """
    Verify that the pre-receive hook in the bare repository is either removed,
    not executable, or exits successfully (0) when run.
    """
    hook_path = "/home/user/cluster-state.git/hooks/pre-receive"

    if os.path.exists(hook_path):
        st = os.stat(hook_path)
        is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        if is_executable:
            try:
                # Run the hook with empty stdin
                result = subprocess.run([hook_path], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                assert result.returncode == 0, "The pre-receive hook is still failing (returns non-zero exit code)."
            except Exception as e:
                pytest.fail(f"Failed to execute pre-receive hook: {e}")

def test_manifest_checked_out():
    """
    Verify that the post-receive hook correctly checked out the manifest
    to the cluster-active directory.
    """
    app_yaml_path = "/home/user/cluster-active/app.yaml"
    assert os.path.isfile(app_yaml_path), f"Manifest was not checked out to {app_yaml_path}. Ensure the post-receive hook is working."

def test_operator_log_output():
    """
    Verify that the operator logged the correct output to cluster-status.log.
    """
    log_path = "/home/user/cluster-status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} not found. Did the operator run and process the webhook?"

    with open(log_path, 'r') as f:
        content = f.read()

    expected_log = "Loaded Deployment: frontend-app"
    assert expected_log in content, f"Log file missing expected exact format: '{expected_log}'. Found: {content}"