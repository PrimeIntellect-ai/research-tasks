# test_final_state.py

import os
import subprocess
import re
import pytest

def test_version_log():
    log_path = "/home/user/version.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "1.2.3", f"Expected version.log to contain '1.2.3', but got '{content}'."

def test_symlink_created():
    symlink_path = "/home/user/libs/libcatalan.so"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    # The target could be absolute or relative, but it must resolve to libcatalan.so.1.2.3
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    expected_target = "/home/user/libs/libcatalan.so.1.2.3"

    assert resolved_target == expected_target, f"Symlink points to {resolved_target}, expected {expected_target}."

def test_catalan_script():
    script_path = "/home/user/catalan.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Test for n=5
    result_5 = subprocess.run(["bash", script_path, "5"], capture_output=True, text=True)
    assert result_5.returncode == 0, f"Running catalan.sh 5 failed with error: {result_5.stderr}"
    assert result_5.stdout.strip() == "42", f"Expected output '42' for n=5, got '{result_5.stdout.strip()}'"

    # Test for n=6
    result_6 = subprocess.run(["bash", script_path, "6"], capture_output=True, text=True)
    assert result_6.returncode == 0, f"Running catalan.sh 6 failed with error: {result_6.stderr}"
    assert result_6.stdout.strip() == "132", f"Expected output '132' for n=6, got '{result_6.stdout.strip()}'"

def test_nginx_config():
    config_path = "/home/user/nginx.conf"
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    # Normalize whitespace for easier matching
    content_normalized = re.sub(r'\s+', ' ', content)

    assert "pid /home/user/nginx.pid;" in content_normalized, "Missing or incorrect pid directive."

    # Check limit_req_zone
    assert re.search(r"limit_req_zone\s+\$binary_remote_addr\s+zone=mylimit:10m\s+rate=2r/s\s*;", content_normalized), \
        "Missing or incorrect limit_req_zone directive."

    # Check limit_req
    assert re.search(r"limit_req\s+zone=mylimit\s*;", content_normalized), \
        "Missing or incorrect limit_req directive."

    # Check proxy_pass
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:9000\s*;", content_normalized), \
        "Missing or incorrect proxy_pass directive."

    # Check listen
    assert re.search(r"listen\s+8080\s*;", content_normalized), \
        "Missing or incorrect listen directive."