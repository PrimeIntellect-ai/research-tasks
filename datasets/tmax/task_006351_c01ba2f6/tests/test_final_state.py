# test_final_state.py

import os
import re
import subprocess
import pytest

def test_generate_nginx_sh_fixed():
    script_path = "/home/user/generate_nginx.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Check if the syntax is valid by running bash -n
    result = subprocess.run(["bash", "-n", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Syntax error in {script_path}: {result.stderr}"

def test_nginx_conf_generated_correctly():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} was not generated"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "location /api/v1 {" in content, "Missing 'location /api/v1 {' in nginx.conf"
    assert 'if ($arg_token != "secret") {' in content, "Missing 'if ($arg_token != \"secret\") {' in nginx.conf"
    assert "proxy_pass http://127.0.0.1:9001;" in content, "Missing 'proxy_pass http://127.0.0.1:9001;' in nginx.conf"
    assert "location /web {" in content, "Missing 'location /web {' in nginx.conf"

def test_bench_log_exists_and_valid():
    log_path = "/home/user/bench.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read()

    assert "ApacheBench" in content, f"{log_path} does not contain ApacheBench output"

def test_fix_patch_exists_and_valid():
    patch_path = "/home/user/fix.patch"
    assert os.path.isfile(patch_path), f"{patch_path} does not exist"

    with open(patch_path, "r") as f:
        content = f.read()

    assert "---" in content, f"{patch_path} does not look like a valid diff (missing '---')"
    assert "+++" in content, f"{patch_path} does not look like a valid diff (missing '+++')"

def test_nginx_is_running():
    # Check if nginx is listening on port 8080 or running
    try:
        result = subprocess.run(["pgrep", "nginx"], capture_output=True, text=True)
        assert result.returncode == 0, "Nginx does not appear to be running"
    except FileNotFoundError:
        pass # pgrep might not be available, skip