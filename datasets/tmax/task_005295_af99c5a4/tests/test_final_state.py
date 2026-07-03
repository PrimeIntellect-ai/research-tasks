# test_final_state.py
import json
import os
import subprocess
import time
import urllib.request
import pytest

WORKSPACE_DIR = "/home/user/workspace"
RESOLUTION_FILE = os.path.join(WORKSPACE_DIR, "resolution.json")
RUST_SO = os.path.join(WORKSPACE_DIR, "rust_lib", "target", "debug", "librustffi.so")
RUST_SRC = os.path.join(WORKSPACE_DIR, "rust_lib", "src", "lib.rs")
PYTHON_API_DIR = os.path.join(WORKSPACE_DIR, "python_api")

def test_resolution_json_exists_and_valid():
    assert os.path.exists(RESOLUTION_FILE), "resolution.json not found at expected path."
    with open(RESOLUTION_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("resolution.json is not valid JSON.")

    expected_keys = {"rust_compile_fix", "memory_leak_fix", "linking_fix"}
    assert expected_keys.issubset(data.keys()), f"resolution.json missing keys. Expected to contain: {expected_keys}"

def test_rust_library_compiled():
    assert os.path.exists(RUST_SO), f"Rust library not found at {RUST_SO}. Did you compile it?"

def test_rust_code_fixes():
    assert os.path.exists(RUST_SRC), f"Rust source file not found at {RUST_SRC}"
    with open(RUST_SRC, "r") as f:
        code = f.read()

    assert "free_text(" in code, "Verification failed: Memory leak not fixed (missing free_text call in Rust code)."
    assert ".into_raw()" in code or "CString::into_raw" in code, "Verification failed: Rust compile fix doesn't use into_raw(), might still return dangling pointer."

def test_python_api_endpoints():
    env = os.environ.copy()
    c_lib_path = os.path.join(WORKSPACE_DIR, "c_lib")
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{c_lib_path}:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = c_lib_path

    proc = subprocess.Popen(
        ["uvicorn", "app:app", "--port", "8000"],
        cwd=PYTHON_API_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Wait for the server to start
        time.sleep(3)
        assert proc.poll() is None, "FastAPI server crashed or failed to start. Check linking or syntax errors."

        # 1. Test /process endpoint
        try:
            req = urllib.request.Request("http://127.0.0.1:8000/process?text=hello")
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, f"Expected status 200, got {response.status}"
                data = json.loads(response.read().decode())
                assert "RUSTIFIED" in data.get("result", ""), "/process endpoint did not return expected RUSTIFIED string."
        except urllib.error.URLError as e:
            pytest.fail(f"/process endpoint request failed: {e}")

        # 2. Test /stats endpoint
        try:
            req_stats = urllib.request.Request("http://127.0.0.1:8000/stats")
            with urllib.request.urlopen(req_stats) as response:
                assert response.status == 200, f"Expected status 200, got {response.status}"
                data = json.loads(response.read().decode())
                assert data.get("status") == "ok", "Expected status 'ok' in /stats response."
                assert data.get("processed_count") == 1, f"Expected processed_count=1 (since /process was called once), got {data.get('processed_count')}"
        except urllib.error.URLError as e:
            pytest.fail(f"/stats endpoint request failed: {e}")

    finally:
        proc.terminate()
        proc.wait()