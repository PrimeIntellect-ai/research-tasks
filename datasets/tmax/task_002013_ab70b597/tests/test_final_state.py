# test_final_state.py
import os
import re

def test_success_log_exists():
    log_path = "/home/user/success.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. Did you run the curl command and save the output?"

def test_success_log_content():
    log_path = "/home/user/success.log"
    with open(log_path, "r") as f:
        content = f.read()

    # Check for the header (case-insensitive)
    assert re.search(r"X-Sandbox-Secure:\s*true", content, re.IGNORECASE), "The 'X-Sandbox-Secure: true' header is missing from the success log."

    # Check for the body
    assert "EXECUTION_SUCCESS" in content, "The body 'EXECUTION_SUCCESS' is missing from the success log."

def test_c_lib_compiled():
    so_path = "/home/user/project/c_lib/libcrypto_dummy.so"
    assert os.path.exists(so_path), f"Shared object {so_path} does not exist. Did you compile the C library?"

def test_nginx_conf_exists():
    conf_path = "/home/user/project/nginx.conf"
    assert os.path.exists(conf_path), f"Nginx config {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "8080" in content, "Nginx config does not seem to listen on port 8080."
    assert "9000" in content, "Nginx config does not seem to proxy to port 9000."