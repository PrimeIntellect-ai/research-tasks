# test_final_state.py
import os
import json
import subprocess
import pytest

def test_phase1_patch_exists():
    patch_file = "/home/user/math_lib/fix.patch"
    assert os.path.isfile(patch_file), f"Patch file {patch_file} is missing"

    # Check if the patch actually applies to the original file
    # We can use patch --dry-run
    orig_file = "/home/user/math_lib/matrix_trace.c.orig"
    assert os.path.isfile(orig_file), "Original C file is missing"

    result = subprocess.run(
        ["patch", "--dry-run", orig_file, "-i", patch_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Patch does not apply cleanly:\n{result.stderr}\n{result.stdout}"

def test_phase1_c_code_fixed():
    c_file = "/home/user/math_lib/matrix_trace.c"
    assert os.path.isfile(c_file), "Modified C file is missing"

    # Compile the C code
    binary = "/home/user/math_lib/matrix_trace_test"
    compile_result = subprocess.run(
        ["gcc", c_file, "-o", binary],
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"C code fails to compile:\n{compile_result.stderr}"

    # Run valgrind to check for memory leaks and errors
    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=1",
        binary
    ]

    # Test input: size 2, matrix: 1 2 3 4
    input_data = "2\n1 2\n3 4\n"
    valgrind_result = subprocess.run(
        valgrind_cmd,
        input=input_data,
        capture_output=True,
        text=True
    )
    assert valgrind_result.returncode == 0, f"Valgrind reported memory errors or leaks:\n{valgrind_result.stderr}"

def test_phase2_run_tests_sh():
    script_file = "/home/user/ci/run_tests.sh"
    assert os.path.isfile(script_file), f"Script {script_file} is missing"
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable"

def test_phase2_results_json():
    results_file = "/home/user/ci/results.json"
    assert os.path.isfile(results_file), f"Results file {results_file} is missing"

    with open(results_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON")

    expected = [
        {"id": "test_1", "trace": 15},
        {"id": "test_2", "trace": 30},
        {"id": "test_3", "trace": 4}
    ]

    assert results == expected, f"Results JSON does not match expected output. Got: {results}"

def test_phase3_nginx_config():
    conf_file = "/home/user/ci/proxy.conf"
    assert os.path.isfile(conf_file), f"Nginx config {conf_file} is missing"

    # Test syntax with nginx -t
    result = subprocess.run(
        ["nginx", "-t", "-c", conf_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Nginx config syntax test failed:\n{result.stderr}"

    # Verify contents manually to ensure requirements are met
    with open(conf_file, "r") as f:
        content = f.read()

    assert "pid /home/user/ci/nginx.pid;" in content or "pid\t/home/user/ci/nginx.pid;" in content or "pid  /home/user/ci/nginx.pid;" in content, "Config missing required pid directive"
    assert "/home/user/ci/error.log" in content, "Config missing required error_log directive"
    assert "/home/user/ci/access.log" in content, "Config missing required access_log directive"
    assert "127.0.0.1:8080" in content, "Config not listening on 127.0.0.1:8080"
    assert "proxy_pass http://127.0.0.1:9090" in content or "proxy_pass http://127.0.0.1:9090/" in content, "Config missing proxy_pass to 127.0.0.1:9090"
    assert "user " not in content, "Config must not contain 'user' directive (unprivileged)"