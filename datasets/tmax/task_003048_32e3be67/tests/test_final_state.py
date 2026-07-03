# test_final_state.py

import os
import tarfile
import re
import pytest

def test_backup_exists_and_valid():
    backup_path = "/home/user/backup/pre_hardening.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} is missing."

    with tarfile.open(backup_path, "r:gz") as tar:
        names = tar.getnames()

    # Check if backend/server.c and nginx/nginx.conf are in the tar
    has_server = any(name.endswith("backend/server.c") for name in names)
    has_nginx = any(name.endswith("nginx/nginx.conf") for name in names)

    assert has_server, "Backup does not contain backend/server.c"
    assert has_nginx, "Backup does not contain nginx/nginx.conf"

def test_nginx_config_hardened():
    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://unix:/home/user/backend/secure.sock;" in content, "Nginx config does not contain the updated secure proxy_pass directive."

def test_c_code_modified_and_secured():
    source_path = "/home/user/backend/server.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    assert "/home/user/backend/secure.sock" in content, "C source does not contain the new secure socket path."

    # Look for chmod with 0600 or 600
    chmod_match = re.search(r"chmod\s*\([^,]+,\s*0?600\s*\)", content)
    assert chmod_match is not None, "C source does not contain a chmod() call setting permissions to 0600."

def test_server_executable_compiled():
    exe_path = "/home/user/backend/server"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_ci_deploy_script_exists_and_executable():
    script_path = "/home/user/ci_deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

def test_pipeline_result_log_correct():
    log_path = "/home/user/pipeline_result.log"
    assert os.path.isfile(log_path), f"Pipeline result log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert '{"status":"secure"}' in content, "Pipeline result log does not contain the expected JSON output."