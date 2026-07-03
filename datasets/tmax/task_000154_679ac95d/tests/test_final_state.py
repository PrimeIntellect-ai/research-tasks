# test_final_state.py

import os
import json
import subprocess
import pytest

def test_provision_script_exists():
    path = '/home/user/provision.py'
    assert os.path.isfile(path), f"File {path} does not exist. You must create the provision script."

def test_deployment_json_updated():
    path = '/home/user/deployment.json'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    services = data.get("services", {})

    backend = services.get("backend", {})
    assert "depends_on" in backend, "Backend service is missing the 'depends_on' key."
    assert "cache" in backend["depends_on"], "Backend 'depends_on' list does not contain 'cache'."
    assert backend["depends_on"].count("cache") == 1, "Backend 'depends_on' contains duplicate 'cache' entries."

    frontend = services.get("frontend", {})
    assert frontend.get("restart_policy") == "always", "Frontend 'restart_policy' was not updated to 'always'."

def test_mock_group_content():
    path = '/home/user/mock_group'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = f.readlines()

    target_line = "deploy_admins:x:1001:app_runner"

    # Strip whitespace to match exactly the content
    stripped_lines = [line.strip() for line in lines]

    assert target_line in stripped_lines, f"The required group '{target_line}' is missing from {path}."
    assert stripped_lines.count(target_line) == 1, f"The group '{target_line}' appears multiple times in {path}. The script must be idempotent."

def test_deploy_success_log():
    path = '/home/user/deploy_success.log'
    assert os.path.isfile(path), f"File {path} does not exist. Did you redirect the runner's output?"

    with open(path, 'r') as f:
        content = f.read()

    expected_msg = "Deployment Successful: All services started in the correct order."
    assert expected_msg in content, f"The success log does not contain the expected message. Found: {content}"

def test_idempotency():
    # Run the student's script again to verify it doesn't break things or duplicate entries
    script_path = '/home/user/provision.py'
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} a second time failed with error: {result.stderr}"

    # Re-verify mock_group
    group_path = '/home/user/mock_group'
    with open(group_path, 'r') as f:
        stripped_lines = [line.strip() for line in f.readlines()]
    target_line = "deploy_admins:x:1001:app_runner"
    assert stripped_lines.count(target_line) == 1, "Running the script a second time created duplicate entries in mock_group."

    # Re-verify deployment.json
    config_path = '/home/user/deployment.json'
    with open(config_path, 'r') as f:
        data = json.load(f)
    backend_depends = data.get("services", {}).get("backend", {}).get("depends_on", [])
    assert backend_depends.count("cache") == 1, "Running the script a second time created duplicate 'cache' entries in deployment.json."