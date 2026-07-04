# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_server_c_fixed():
    server_c_path = "/home/user/app/server.c"
    assert os.path.isfile(server_c_path), f"{server_c_path} is missing"
    with open(server_c_path, "r") as f:
        content = f.read()
    assert "/home/user/run/app.sock" in content, f"{server_c_path} does not contain the correct socket path '/home/user/run/app.sock'"
    assert "/tmp/wrong.sock" not in content, f"{server_c_path} still contains the old wrong socket path"

def test_nginx_conf_fixed():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"{nginx_conf_path} is missing"
    with open(nginx_conf_path, "r") as f:
        content = f.read()
    assert "/home/user/run/app.sock" in content, f"{nginx_conf_path} does not contain the correct socket path '/home/user/run/app.sock'"

def test_run_dir_permissions():
    run_dir = "/home/user/run"
    assert os.path.isdir(run_dir), f"{run_dir} directory is missing"
    st = os.stat(run_dir)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o700, f"{run_dir} permissions are {oct(permissions)}, expected 0o700"

def test_setup_sh_exists_and_executable():
    setup_sh_path = "/home/user/setup.sh"
    assert os.path.isfile(setup_sh_path), f"{setup_sh_path} is missing"
    assert os.access(setup_sh_path, os.X_OK), f"{setup_sh_path} is not executable"

def test_setup_sh_idempotent_execution():
    setup_sh_path = "/home/user/setup.sh"
    # Run the script to verify it is idempotent and completes successfully
    result = subprocess.run([setup_sh_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{setup_sh_path} failed to execute properly. Error: {result.stderr}"

def test_success_log_content():
    success_log_path = "/home/user/success.log"
    assert os.path.isfile(success_log_path), f"{success_log_path} is missing"
    with open(success_log_path, "r") as f:
        content = f.read().strip()
    assert content == "Hello Microservice", f"{success_log_path} contains '{content}', expected exactly 'Hello Microservice'"