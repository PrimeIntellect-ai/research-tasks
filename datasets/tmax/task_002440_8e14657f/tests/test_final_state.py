# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_config_secure_json():
    secure_config_path = '/home/user/project/config_secure.json'
    assert os.path.isfile(secure_config_path), f"File missing: {secure_config_path}"

    with open(secure_config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{secure_config_path} is not valid JSON")

    assert "credentials" in data, "Missing 'credentials' object in secure config"
    creds = data["credentials"]

    assert creds.get("api_key") == "***MASKED***", "api_key was not properly masked"
    assert creds.get("password") == "***MASKED***", "password was not properly masked"
    assert creds.get("user") == "admin", "user key was modified or is missing"
    assert data.get("app") == "my_app", "app key was modified or is missing"

def test_patch_applied():
    server_js_path = '/home/user/project/src/server.js'
    assert os.path.isfile(server_js_path), f"File missing: {server_js_path}"

    with open(server_js_path, 'r') as f:
        content = f.read()

    assert "app.disable('x-powered-by');" in content, "The security patch was not successfully applied to server.js"

def test_leaked_file_deleted():
    leaked_script_path = '/home/user/project/src/leaked_script.py'
    assert not os.path.exists(leaked_script_path), f"The leaked file {leaked_script_path} was not deleted"

def test_deleted_file_log():
    log_path = '/home/user/project/deleted_file.log'
    assert os.path.isfile(log_path), f"File missing: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "leaked_script.py", f"Expected 'leaked_script.py' in {log_path}, got '{content}'"

def test_ci_check_script():
    script_path = '/home/user/project/ci_check.sh'
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

    # Run script in current state (no secrets should be present)
    result = subprocess.run([script_path], cwd='/home/user/project', capture_output=True)
    assert result.returncode == 0, f"Script {script_path} returned {result.returncode} instead of 0 when no secrets are present"

    # Temporarily create a file with a secret to test if it detects it
    test_secret_file = '/home/user/project/src/temp_test_secret.txt'
    try:
        with open(test_secret_file, 'w') as f:
            f.write("Here is a SECRET_123 string")

        result_with_secret = subprocess.run([script_path], cwd='/home/user/project', capture_output=True)
        assert result_with_secret.returncode == 1, f"Script {script_path} did not return 1 when a secret was introduced"
    finally:
        if os.path.exists(test_secret_file):
            os.remove(test_secret_file)