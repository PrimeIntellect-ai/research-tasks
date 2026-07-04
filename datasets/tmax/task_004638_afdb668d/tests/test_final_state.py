# test_final_state.py

import os
import time
import json
import subprocess
import pytest

def test_bashrc_env_var():
    bashrc_path = '/home/user/.bashrc'
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist"
    with open(bashrc_path, 'r') as f:
        content = f.read()
    assert 'ROUTER_LOG_PATH' in content, "ROUTER_LOG_PATH not found in .bashrc"

def test_acl_permissions():
    log_path = "/app/secure_logs/router.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist"

    # Check ACL for the directory
    dir_result = subprocess.run(["getfacl", "/app/secure_logs"], capture_output=True, text=True)
    assert "user:user:r" in dir_result.stdout, "User does not have read ACL on /app/secure_logs"
    assert "user:user:--x" in dir_result.stdout or "user:user:r-x" in dir_result.stdout or "user:user:rwx" in dir_result.stdout, "User does not have execute ACL on /app/secure_logs"

    # Check ACL for the file
    file_result = subprocess.run(["getfacl", log_path], capture_output=True, text=True)
    assert "user:user:r" in file_result.stdout, f"User does not have read ACL on {log_path}"

def test_health_file():
    health_path = '/tmp/analyzer.health'
    assert os.path.exists(health_path), f"Health file {health_path} not found"
    with open(health_path, 'r') as f:
        content = f.read()
    assert 'OK' in content, f"Health file does not contain 'OK'. Found: {content}"

def test_analysis_json():
    json_path = '/tmp/analysis.json'
    assert os.path.exists(json_path), f"Output {json_path} not found"
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON")

def test_binary_execution_time():
    binary_path = "/app/vendored/net-analyzer/target/release/net-analyzer"
    assert os.path.exists(binary_path), f"Binary not found at {binary_path}. Did you compile with --release?"

    env = os.environ.copy()
    env["ROUTER_LOG_PATH"] = "/app/secure_logs/router.log"

    start = time.time()
    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)
    duration = time.time() - start

    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert duration <= 0.5, f"Execution time {duration:.3f}s exceeded threshold of 0.5s"