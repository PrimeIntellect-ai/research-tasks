# test_final_state.py

import os
import subprocess
import pytest

def test_shared_library_built():
    so_path = "/home/user/workspace/c_math/build/libcmath.so"
    assert os.path.isfile(so_path), f"Shared library not found at {so_path}. Did you compile the CMake project?"

def test_build_rs_exists_and_correct():
    build_rs_path = "/home/user/workspace/api/build.rs"
    assert os.path.isfile(build_rs_path), f"build.rs not found at {build_rs_path}."
    with open(build_rs_path, "r") as f:
        content = f.read()
    assert "cargo:rustc-link-search" in content, "build.rs is missing cargo:rustc-link-search instruction."
    assert "cargo:rustc-link-lib" in content, "build.rs is missing cargo:rustc-link-lib instruction."

def test_e2e_test_exists_and_correct():
    test_path = "/home/user/workspace/api/tests/e2e_test.rs"
    assert os.path.isfile(test_path), f"e2e_test.rs not found at {test_path}."
    with open(test_path, "r") as f:
        content = f.read()
    assert "proptest" in content, "e2e_test.rs does not seem to use proptest."
    assert "reqwest" in content, "e2e_test.rs does not seem to use reqwest."
    assert "test_add_sub_inverse" in content, "e2e_test.rs is missing the test_add_sub_inverse test."

def test_run_all_script():
    script_path = "/home/user/workspace/run_all.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True, cwd="/home/user/workspace")
    assert result.returncode == 0, f"run_all.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    status_path = "/home/user/workspace/status.txt"
    assert os.path.isfile(status_path), f"status.txt not found at {status_path}."
    with open(status_path, "r") as f:
        status_content = f.read()

    assert status_content == "SUCCESS\n" or status_content == "SUCCESS", f"Expected status.txt to contain 'SUCCESS', but got {repr(status_content)}."