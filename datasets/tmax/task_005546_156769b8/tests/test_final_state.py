# test_final_state.py

import os
import json
import urllib.request
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
LEGACY_CRYPTO_DIR = os.path.join(WORKSPACE_DIR, "legacy_crypto")
RUST_API_DIR = os.path.join(WORKSPACE_DIR, "rust_api")

def test_phase1_shared_library_built():
    so_path = os.path.join(LEGACY_CRYPTO_DIR, "libcrypto_mask.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

    # Check if it's actually a shared object
    result = subprocess.run(["file", so_path], capture_output=True, text=True)
    assert "shared object" in result.stdout, f"{so_path} is not a valid shared object. file output: {result.stdout}"

def test_phase2_rust_api_tests_pass():
    assert os.path.isdir(RUST_API_DIR), f"Rust API directory {RUST_API_DIR} is missing."

    # Run cargo test
    env = os.environ.copy()
    ld_lib_path = env.get("LD_LIBRARY_PATH", "")
    env["LD_LIBRARY_PATH"] = f"{LEGACY_CRYPTO_DIR}:{ld_lib_path}".strip(":")

    result = subprocess.run(
        ["cargo", "test"],
        cwd=RUST_API_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rust unit tests failed or did not run.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_phase2_rust_server_endpoint():
    # Test the running server
    url = "http://127.0.0.1:8080/secure-token"
    payload = json.dumps({"token": "test"}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            data = json.loads(resp_body)
            assert "masked" in data, "Response JSON does not contain 'masked' field."

            # Compute expected mask for "test"
            # 't' = 116 ^ 42 = 94 ('^')
            # 'e' = 101 ^ 42 = 79 ('O')
            # 's' = 115 ^ 42 = 89 ('Y')
            # 't' = 116 ^ 42 = 94 ('^')
            expected_masked = "^OY^"
            assert data["masked"] == expected_masked, f"Expected masked value '{expected_masked}', got '{data['masked']}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Rust server at {url}: {e}")
    except json.JSONDecodeError:
        pytest.fail(f"Server at {url} did not return valid JSON.")

def test_phase3_go_benchmark_script_exists():
    bench_go = os.path.join(WORKSPACE_DIR, "bench.go")
    assert os.path.isfile(bench_go), f"Go benchmark script {bench_go} is missing."

def test_phase3_benchmark_report():
    report_path = os.path.join(WORKSPACE_DIR, "bench_report.txt")
    assert os.path.isfile(report_path), f"Benchmark report {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert "Success: 500" in content, f"Expected 'Success: 500' in {report_path}, found: '{content}'"