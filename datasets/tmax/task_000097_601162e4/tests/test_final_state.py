# test_final_state.py

import os
import subprocess
import ctypes
import time
import urllib.request
import urllib.error
import pytest
import signal

def test_files_exist():
    assert os.path.isfile("/home/user/trie.c"), "/home/user/trie.c is missing"
    assert os.path.isfile("/home/user/Makefile"), "/home/user/Makefile is missing"
    assert os.path.isfile("/home/user/proxy.py"), "/home/user/proxy.py is missing"

def test_make_and_libtrie():
    # Run make
    result = subprocess.run(["make"], cwd="/home/user", capture_output=True)
    assert result.returncode == 0, f"make failed: {result.stderr.decode()}"
    assert os.path.isfile("/home/user/libtrie.so"), "/home/user/libtrie.so was not built"

def test_trie_c_extension():
    # Ensure libtrie.so is built
    subprocess.run(["make"], cwd="/home/user", capture_output=True)
    lib_path = "/home/user/libtrie.so"
    assert os.path.isfile(lib_path), f"{lib_path} is missing"

    try:
        trie_lib = ctypes.CDLL(lib_path)
    except OSError as e:
        pytest.fail(f"Failed to load {lib_path}: {e}")

    # Set up function signatures
    trie_lib.trie_create.restype = ctypes.c_void_p
    trie_lib.trie_insert.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    trie_lib.trie_check.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    trie_lib.trie_check.restype = ctypes.c_int

    trie = trie_lib.trie_create()
    assert trie is not None, "trie_create returned NULL"

    trie_lib.trie_insert(trie, b"/admin")
    trie_lib.trie_insert(trie, b"/private/")

    assert trie_lib.trie_check(trie, b"/admin") == 1, "trie_check failed to match /admin"
    assert trie_lib.trie_check(trie, b"/admin/dashboard") == 1, "trie_check failed to match prefix /admin/dashboard"
    assert trie_lib.trie_check(trie, b"/private/data") == 1, "trie_check failed to match /private/data"
    assert trie_lib.trie_check(trie, b"/public") == 0, "trie_check incorrectly matched /public"
    assert trie_lib.trie_check(trie, b"/priv") == 0, "trie_check incorrectly matched partial prefix /priv"

@pytest.fixture(scope="module")
def servers():
    # Build libtrie.so just in case
    subprocess.run(["make"], cwd="/home/user", capture_output=True)

    # Start backend server
    backend = subprocess.Popen(
        ["python3", "-m", "http.server", "9090", "--bind", "127.0.0.1"],
        cwd="/home/user/backend",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Start proxy server
    proxy = subprocess.Popen(
        ["python3", "proxy.py"],
        cwd="/home/user",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for servers to start
    time.sleep(2)

    yield

    # Teardown
    proxy.terminate()
    backend.terminate()
    proxy.wait()
    backend.wait()

def fetch_url(path):
    url = f"http://127.0.0.1:8080{path}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy: {e}")

def test_proxy_allowed_paths(servers):
    status, body = fetch_url("/index.html")
    assert status == 200, f"Expected status 200 for /index.html, got {status}"
    assert "OK" in body, "Expected 'OK' in response body for /index.html"

    status, body = fetch_url("/public.txt")
    assert status == 200, f"Expected status 200 for /public.txt, got {status}"
    assert "PUBLIC" in body, "Expected 'PUBLIC' in response body for /public.txt"

    status, body = fetch_url("/api/v1/public")
    assert status == 404, f"Expected status 404 for missing file /api/v1/public, got {status}"

def test_proxy_blocked_paths(servers):
    blocked_paths = [
        "/admin",
        "/admin.html",
        "/private/data",
        "/api/v1/secret/keys"
    ]

    for path in blocked_paths:
        status, body = fetch_url(path)
        assert status == 403, f"Expected status 403 for blocked path {path}, got {status}"
        assert "Blocked by Trie" in body, f"Expected 'Blocked by Trie' in response body for {path}"