# test_final_state.py

import os
import ctypes
import urllib.request
import urllib.error
import pytest

def test_makefile_exists():
    assert os.path.exists("/home/user/project/Makefile"), "Makefile is missing"

def test_libfilter_so_exists():
    assert os.path.exists("/home/user/project/libfilter.so"), "libfilter.so is missing. Did the Makefile build it?"

def test_rust_service_exists():
    assert os.path.exists("/home/user/project/service/target/release/math_service"), "math_service executable is missing"

def test_nginx_config():
    assert os.path.exists("/etc/nginx/sites-enabled/math_proxy"), "Nginx config /etc/nginx/sites-enabled/math_proxy is missing"

def test_ctypes_validate_math():
    lib_path = "/home/user/project/libfilter.so"
    assert os.path.exists(lib_path), f"{lib_path} not found"

    try:
        lib = ctypes.CDLL(lib_path)
    except Exception as e:
        pytest.fail(f"Failed to load {lib_path}: {e}")

    assert hasattr(lib, "validate_math"), "validate_math function not found in libfilter.so"

    lib.validate_math.argtypes = [ctypes.c_char_p]
    lib.validate_math.restype = ctypes.c_int

    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_failed = []
    for f in os.listdir(clean_dir):
        with open(os.path.join(clean_dir, f), "rb") as file:
            content = file.read().strip()
            if lib.validate_math(content) != 1:
                clean_failed.append(f)

    evil_failed = []
    for f in os.listdir(evil_dir):
        with open(os.path.join(evil_dir, f), "rb") as file:
            content = file.read().strip()
            if lib.validate_math(content) != 0:
                evil_failed.append(f)

    err_msg = []
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} evil bypassed: {', '.join(evil_failed)}")

    if err_msg:
        pytest.fail(" | ".join(err_msg))

def test_web_endpoint():
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    url = "http://127.0.0.1:8080/eval"

    clean_failed = []
    for f in os.listdir(clean_dir):
        with open(os.path.join(clean_dir, f), "rb") as file:
            content = file.read().strip()
            req = urllib.request.Request(url, data=content, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=2) as response:
                    if response.status != 200:
                        clean_failed.append(f)
            except Exception:
                clean_failed.append(f)

    evil_failed = []
    for f in os.listdir(evil_dir):
        with open(os.path.join(evil_dir, f), "rb") as file:
            content = file.read().strip()
            req = urllib.request.Request(url, data=content, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=2) as response:
                    if response.status == 200:
                        evil_failed.append(f)
            except urllib.error.HTTPError as e:
                if e.code != 400:
                    evil_failed.append(f)
            except Exception:
                pass # Other exceptions like connection reset are acceptable for evil

    err_msg = []
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} clean modified/rejected via web: {', '.join(clean_failed)}")
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} evil bypassed via web: {', '.join(evil_failed)}")

    if err_msg:
        pytest.fail(" | ".join(err_msg))