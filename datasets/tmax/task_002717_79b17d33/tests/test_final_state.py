# test_final_state.py

import os

def test_status_log_exists_and_correct():
    log_path = "/home/user/status.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did the supervisor run successfully and start the worker?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "STATUS: MIGRATION_SUCCESS" in content, f"The file {log_path} does not contain the expected success message. Content found: {content}"

def test_supervisor_modifications():
    supervisor_path = "/home/user/supervisor.py"
    assert os.path.isfile(supervisor_path), f"Missing file: {supervisor_path}"

    with open(supervisor_path, "r") as f:
        content = f.read()

    # Check for readiness checking logic (e.g. socket)
    assert "socket" in content, "The supervisor.py script does not seem to import or use 'socket' for readiness checking."

    # Check for environment variable logic
    assert "env" in content or "environ" in content, "The supervisor.py script does not seem to handle environment variables (missing 'env' or 'environ')."