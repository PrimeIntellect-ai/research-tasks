# test_final_state.py

import ctypes
import os
import subprocess
import pytest

def test_filter_corpus():
    filter_src = "/app/proxy/filter.c"
    assert os.path.isfile(filter_src), f"Missing filter source file at {filter_src}"

    lib_path = "/tmp/libfilter.so"
    compile_cmd = ["gcc", "-shared", "-fPIC", filter_src, "-o", lib_path]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile filter.c:\n{e.stderr}")

    lib = ctypes.CDLL(lib_path)
    validate_payload = lib.validate_payload
    validate_payload.argtypes = [ctypes.c_char_p]
    validate_payload.restype = ctypes.c_int

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for f in clean_files:
        with open(os.path.join(clean_dir, f), 'rb') as fd:
            data = fd.read()
            if validate_payload(data) != 0:
                clean_failed.append(f)

    evil_failed = []
    for f in evil_files:
        with open(os.path.join(evil_dir, f), 'rb') as fd:
            data = fd.read()
            if validate_payload(data) != 1:
                evil_failed.append(f)

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed[:10])}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed[:10])}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_proxy_auth_header_in_source():
    proxy_dir = "/app/proxy/"
    assert os.path.isdir(proxy_dir), f"Missing proxy directory at {proxy_dir}"

    found = False
    for f in os.listdir(proxy_dir):
        if f.endswith(".c") or f.endswith(".h"):
            filepath = os.path.join(proxy_dir, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fd:
                content = fd.read().lower()
                if "blackberry" in content:
                    found = True
                    break

    assert found, "The transcribed word 'blackberry' was not found in the proxy source code. Expected the header X-Proxy-Auth: blackberry to be injected."

def test_build_and_run_script_exists():
    script_path = "/app/build_and_run.sh"
    assert os.path.isfile(script_path), f"Missing deployment script at {script_path}"

    with open(script_path, 'r', encoding='utf-8', errors='ignore') as fd:
        content = fd.read()
        assert "gcc" in content, "Deployment script does not contain a 'gcc' command to compile the proxy."
        assert "c-proxy" in content, "Deployment script does not compile to an executable named 'c-proxy'."
        assert "go run" in content or "go build" in content or "backend" in content, "Deployment script does not appear to start the Go backend."