# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE = "/home/user/workspace"

def test_venv_exists():
    venv_dir = os.path.join(WORKSPACE, "venv")
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    python_bin = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found in {venv_dir}."

def test_requirements_txt():
    req_path = os.path.join(WORKSPACE, "requirements.txt")
    assert os.path.isfile(req_path), f"{req_path} does not exist."
    with open(req_path, "r") as f:
        content = f.read().lower()

    for pkg in ["flask", "requests", "pytest", "hypothesis"]:
        assert pkg in content, f"Package {pkg} is missing from requirements.txt."

def test_pytest_passes():
    pytest_bin = os.path.join(WORKSPACE, "venv", "bin", "pytest")
    test_file = os.path.join(WORKSPACE, "test_tree.py")

    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."
    assert os.path.isfile(pytest_bin), f"pytest executable not found at {pytest_bin}."

    result = subprocess.run([pytest_bin, test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed on {test_file}:\n{result.stdout}\n{result.stderr}"

def test_nginx_config_valid():
    nginx_conf = os.path.join(WORKSPACE, "nginx.conf")
    assert os.path.isfile(nginx_conf), f"Nginx config {nginx_conf} does not exist."

    result = subprocess.run(["nginx", "-t", "-c", nginx_conf], capture_output=True, text=True)
    assert result.returncode == 0, f"Nginx config syntax check failed:\n{result.stderr}"

def test_uploader_binary_exists():
    uploader_bin = os.path.join(WORKSPACE, "uploader")
    assert os.path.isfile(uploader_bin), f"Compiled Go binary {uploader_bin} does not exist."
    assert os.access(uploader_bin, os.X_OK), f"File {uploader_bin} is not executable."

def test_final_result_log():
    log_path = os.path.join(WORKSPACE, "final_result.log")
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON: {content}")

    assert "version" in data, f"'version' key missing in final_result.log JSON: {data}"
    assert data["version"] == "1.0.12", f"Expected version '1.0.12', but got '{data['version']}'."