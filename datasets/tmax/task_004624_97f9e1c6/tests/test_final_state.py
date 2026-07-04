# test_final_state.py

import os
import stat
import pytest

def test_auth_key_permissions():
    key_path = "/home/user/auth_key.key"
    assert os.path.exists(key_path), f"Missing file: {key_path}"

    st = os.stat(key_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Expected permissions 0o400 on {key_path}, but got {oct(permissions)}"

def test_analyze_script_exists():
    script_path = "/home/user/analyze.py"
    assert os.path.exists(script_path), f"Missing script file: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"

def test_investigation_result_log():
    log_path = "/home/user/investigation_result.log"
    assert os.path.exists(log_path), f"Missing log file: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_endpoint = "/api/v3/hidden_command_c2_991x"
    assert content == expected_endpoint, f"Expected log content '{expected_endpoint}', but got '{content}'"