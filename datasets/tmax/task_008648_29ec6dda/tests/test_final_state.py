# test_final_state.py
import os
import subprocess
import socket
import re

def test_merger_binary_exists_and_executable():
    path = "/home/user/merger"
    assert os.path.isfile(path), f"Compiled binary not found at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_merger_logic_fixed():
    # Test the binary directly to ensure the duplicate dropping bug is fixed
    binary_path = "/home/user/merger"
    assert os.path.isfile(binary_path), f"Binary {binary_path} missing"

    process = subprocess.Popen(
        [binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, _ = process.communicate(input="1 2 2 3\n2 3 4\n")

    expected = "1 2 2 2 3 3 4\n"
    actual = stdout
    assert actual == expected, f"Binary logic incorrect. Expected '{expected.strip()}', got '{actual.strip()}'"

def test_nginx_config_exists_and_valid():
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"Nginx config not found at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "stream" in content, "Nginx config does not contain a 'stream' block"
    assert "8080" in content, "Nginx config does not mention port 8080"
    assert "9000" in content, "Nginx config does not mention port 9000"

def test_nginx_listening_on_8080():
    try:
        with socket.create_connection(("127.0.0.1", 8080), timeout=2):
            pass
    except OSError:
        assert False, "Nginx (or a service) is not listening on 127.0.0.1:8080"

def test_socat_listening_on_9000():
    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=2):
            pass
    except OSError:
        assert False, "socat (or a service) is not listening on 127.0.0.1:9000"

def test_end_to_end_proxy():
    # Send data to 8080, it should be proxied to 9000 and processed by merger
    try:
        s = socket.create_connection(("127.0.0.1", 8080), timeout=2)
        s.sendall(b"1 5 9\n2 5 8\n")
        data = s.recv(1024).decode('utf-8')
        s.close()
    except Exception as e:
        assert False, f"End-to-end proxy test failed with exception: {e}"

    expected = "1 2 5 5 8 9\n"
    assert data == expected, f"End-to-end proxy test failed. Expected '{expected.strip()}', got '{data.strip()}'"

def test_test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"Test results log not found at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "1 passed" in content or "passed" in content.lower(), "Test results log does not indicate a passing test"

def test_fix_patch_exists_and_valid():
    path = "/home/user/fix.patch"
    assert os.path.isfile(path), f"Patch file not found at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, "Patch file does not appear to be a valid unified diff"
    assert "merger.c" in content, "Patch file does not reference merger.c"