# test_final_state.py

import os
import json
import pytest

def test_go_code_fixed():
    main_go_path = "/home/user/vnc-api/main.go"
    assert os.path.isfile(main_go_path), f"{main_go_path} is missing"

    with open(main_go_path, 'r') as f:
        content = f.read()

    assert "/home/user/vnc-api/certs/server.crt" in content, "main.go does not contain the correct path for server.crt"
    assert "/home/user/vnc-api/certs/server.key" in content, "main.go does not contain the correct path for server.key"
    assert "/etc/ssl/certs/server.crt" not in content, "main.go still contains the hardcoded incorrect cert path"

def test_certs_exist():
    cert_path = "/home/user/vnc-api/certs/server.crt"
    key_path = "/home/user/vnc-api/certs/server.key"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing"
    assert os.path.isfile(key_path), f"Key file {key_path} is missing"
    assert os.path.getsize(cert_path) > 0, f"Certificate file {cert_path} is empty"
    assert os.path.getsize(key_path) > 0, f"Key file {key_path} is empty"

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Deploy script {script_path} is not executable"

def test_vnc_manager_compiled_and_logged():
    binary_path = "/home/user/vnc-api/vnc-manager"
    log_path = "/home/user/vnc-api/api.log"

    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing"
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing"

def test_result_json():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"{result_path} does not contain valid JSON")

    expected_data = {"service": "vnc-manager", "status": "running", "active_vms": 0}
    assert data == expected_data, f"Content of {result_path} does not match the expected API output"