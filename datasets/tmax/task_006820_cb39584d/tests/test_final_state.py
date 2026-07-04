# test_final_state.py

import os
import json
import pytest

def test_verify_auth_script_exists_and_executable():
    script_path = "/home/user/verify_auth.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_verify_auth_script_contains_env_i():
    script_path = "/home/user/verify_auth.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()
    assert "env -i" in content, f"Script {script_path} does not contain 'env -i' as required for process isolation."

def test_verification_result_log():
    log_path = "/home/user/verification_result.log"
    assert os.path.isfile(log_path), f"Result log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON. Found: {content}")

    assert data.get("authenticated") is True, f"Expected {{\"authenticated\": true}} in {log_path}, but got {content}"