# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import time
import pytest

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/matrix_app/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deployment script {deploy_script} does not exist."
    st = os.stat(deploy_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script {deploy_script} is not executable."

def test_abi_version_file():
    abi_file = "/home/user/matrix_app/abi_version.txt"
    assert os.path.isfile(abi_file), f"ABI version file {abi_file} does not exist."
    with open(abi_file, "r") as f:
        content = f.read().strip()
    assert "libcompute_v2.so" in content, f"Expected 'libcompute_v2.so' in {abi_file}, got '{content}'."

def test_symlink_correct():
    symlink_path = "/home/user/matrix_app/libs/libcompute.so"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    target = os.readlink(symlink_path)
    assert target.endswith("libcompute_v2.so"), f"Symlink points to {target}, expected it to point to libcompute_v2.so."

def test_server_compiled():
    server_bin = "/home/user/matrix_app/server"
    assert os.path.isfile(server_bin), f"Compiled server binary {server_bin} does not exist."
    st = os.stat(server_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"Server binary {server_bin} is not executable."

def test_reverse_proxy_and_server_response():
    url = "http://127.0.0.1:9090"
    max_retries = 5
    response_body = ""

    for _ in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                response_body = response.read().decode('utf-8')
                break
        except Exception as e:
            time.sleep(1)
            continue
    else:
        pytest.fail(f"Failed to connect to {url} or receive a successful response. Ensure the server and socat proxy are running.")

    assert "Matrix Computed" in response_body, f"Expected 'Matrix Computed' in response, got '{response_body}'."