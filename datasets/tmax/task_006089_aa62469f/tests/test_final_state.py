# test_final_state.py

import os
import re

def test_mock_passwd_updated():
    """Verify mock_passwd contains exactly one instance of the new nginx_user."""
    file_path = "/home/user/mock_passwd"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    expected_line = "nginx_user:x:1005:1005:Nginx Dummy User:/home/user/nginx:/bin/false"

    # Check that the line exists
    assert expected_line in content, f"'{expected_line}' not found in {file_path}."

    # Check that it only appears exactly once (idempotent addition)
    count = content.count(expected_line)
    assert count == 1, f"Expected exactly 1 occurrence of the nginx_user line in {file_path}, found {count}."

def test_tls_certs_exist():
    """Verify that the TLS certificate and key have been created."""
    crt_path = "/home/user/nginx/certs/server.crt"
    key_path = "/home/user/nginx/certs/server.key"

    assert os.path.isfile(crt_path), f"TLS certificate {crt_path} is missing."
    assert os.path.isfile(key_path), f"TLS private key {key_path} is missing."

    # Basic check that files are not empty
    assert os.path.getsize(crt_path) > 0, f"TLS certificate {crt_path} is empty."
    assert os.path.getsize(key_path) > 0, f"TLS private key {key_path} is empty."

def test_nginx_conf_fixed():
    """Verify that nginx.conf has been updated to point to the correct backend port (8000)."""
    file_path = "/home/user/nginx/conf/nginx.conf"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:8000;" in content, "nginx.conf does not contain the corrected proxy_pass directive pointing to port 8000."
    assert "proxy_pass http://127.0.0.1:9999;" not in content, "nginx.conf still contains the misconfigured proxy_pass directive pointing to port 9999."

def test_proxy_test_log():
    """Verify that proxy_test.log exists and contains the correct backend response."""
    file_path = "/home/user/proxy_test.log"
    assert os.path.isfile(file_path), f"{file_path} is missing. Did you run the curl command and redirect output?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "Backend Application Running!"
    assert content == expected_content, f"Expected '{expected_content}' in {file_path}, but got '{content}'."

def test_idempotent_setup_script_exists():
    """Verify that the idempotent_setup.py script was created."""
    file_path = "/home/user/idempotent_setup.py"
    assert os.path.isfile(file_path), f"{file_path} is missing."