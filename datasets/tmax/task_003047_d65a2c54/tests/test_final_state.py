# test_final_state.py

import os
import re
import subprocess
import pytest

def test_cpp_service_updated():
    cpp_path = "/home/user/service/main.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."
    with open(cpp_path, "r") as f:
        content = f.read()
    assert "/home/user/service/backend.sock" in content, "The C++ service was not updated to use the correct socket path."
    assert "/home/user/service/wrong.sock" not in content, "The C++ service still contains the wrong socket path."

def test_nginx_config():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File {nginx_conf_path} is missing."
    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Check listening port
    assert re.search(r"listen\s+8080\s*;", content), "Nginx is not configured to listen on port 8080."

    # Check proxy pass
    assert re.search(r"proxy_pass\s+http://unix:/home/user/service/backend\.sock\s*;", content), "Nginx is not proxying to the correct backend.sock."

    # Check access control
    assert re.search(r"allow\s+127\.0\.0\.1\s*;", content), "Nginx config missing 'allow 127.0.0.1;'."
    assert re.search(r"deny\s+all\s*;", content), "Nginx config missing 'deny all;'."

def test_services_running():
    # Check processes
    ps_output = subprocess.check_output(["ps", "aux"], text=True)
    assert "nginx" in ps_output, "Nginx is not running."
    assert "socat" in ps_output, "socat is not running."
    assert "backend_service" in ps_output or "./backend_service" in ps_output or "main" in ps_output, "The C++ backend service is not running."

    # Check listening ports
    ss_output = subprocess.check_output(["ss", "-tln"], text=True)
    assert ":8080" in ss_output, "Nothing is listening on port 8080 (expected Nginx)."
    assert ":9090" in ss_output, "Nothing is listening on port 9090 (expected socat)."

def test_migration_status():
    target_path = "/home/user/data/migration_target.txt"
    status_path = "/home/user/data/migration_status.txt"

    assert os.path.isfile(target_path), f"File {target_path} is missing."
    with open(target_path, "r") as f:
        target_content = f.read().strip()

    assert os.path.isfile(status_path), f"File {status_path} is missing. The API was likely not triggered or the C++ service failed to write it."
    with open(status_path, "r") as f:
        status_content = f.read().strip()

    expected_status = f"MIGRATION_COMPLETE_TO_{target_content}"
    assert status_content == expected_status, f"Expected status '{expected_status}', but got '{status_content}'."

def test_test_result():
    result_path = "/home/user/test_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you save the curl output?"
    with open(result_path, "r") as f:
        content = f.read().strip()
    assert content == "Success", f"Expected test result to be 'Success', but got '{content}'."