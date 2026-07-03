# test_final_state.py

import os
import pytest

def test_results_log():
    """Verify that the results.log contains the correct HTTP status codes."""
    log_path = "/home/user/deployment_test/results.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run test.sh and redirect output?"

    with open(log_path, "r") as f:
        content = f.read().strip().split()

    expected = ["200", "426", "200", "200"]
    assert content == expected, f"Expected results.log to contain {expected}, but got {content}. This indicates either the backend logic or the nginx routing is incorrect."

def test_backend_c_fixed():
    """Verify that backend.c no longer uses the naive strcmp implementation."""
    file_path = "/home/user/deployment_test/backend.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "strcmp(version, min_version)" not in content, "backend.c still contains the buggy strcmp implementation for check_version."

def test_nginx_conf_exists_and_valid():
    """Verify that nginx.conf exists and contains required configurations."""
    conf_path = "/home/user/deployment_test/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing. Did you create the Nginx configuration?"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "8080" in content, "nginx.conf does not seem to listen on port 8080."
    assert "X-API-Version" in content, "nginx.conf does not seem to set the X-API-Version header."
    assert "9090" in content, "nginx.conf does not seem to proxy to the backend port 9090."