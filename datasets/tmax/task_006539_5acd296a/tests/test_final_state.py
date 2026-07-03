# test_final_state.py
import os
import subprocess
import pytest

def test_proxy_cpp_fixed():
    path = "/home/user/src/proxy.cpp"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "htons(8080)" in content, "proxy.cpp does not bind to port 8080. You need to change htons(80) to htons(8080)."

def test_backends_conf_content():
    path = "/home/user/proxy_config/backends.conf"
    assert os.path.isfile(path), f"File {path} is missing. Did the mount script run correctly?"
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 1, f"backends.conf should contain exactly one line, found {len(lines)}."
    assert lines[0] == "127.0.0.1:9001", f"backends.conf does not contain the correct IP:PORT. Found: {lines[0]}"

def test_acl_set_correctly():
    path = "/home/user/proxy_config/backends.conf"
    assert os.path.isfile(path), f"File {path} is missing."

    try:
        result = subprocess.run(["getfacl", path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run getfacl on {path}: {e}")

    acl_output = result.stdout
    # We are looking for user:nobody:r-- or user:nobody:rw- etc.
    # The requirement is that nobody has read access.
    has_read = False
    for line in acl_output.splitlines():
        if line.startswith("user:nobody:") and len(line) >= 13 and line[12] == "r":
            has_read = True
            break

    assert has_read, f"ACL for user 'nobody' does not grant read access. getfacl output:\n{acl_output}"

def test_final_output_file():
    path = "/home/user/final_proxy_output.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you save the curl output?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert "Hello from backend!" in content, "final_proxy_output.txt does not contain the expected response from the proxy."