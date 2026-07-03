# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_rust_compilation():
    """Verify that the Rust project compiles successfully after fixing the FFI signature."""
    result = subprocess.run(
        ["cargo", "build"], 
        cwd=PROJECT_DIR, 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"Cargo build failed. The FFI signature might still be incorrect.\nStderr:\n{result.stderr}"

def test_c_memory_safety_fix():
    """Verify that the C code uses dynamic memory allocation to fix the memory safety bug."""
    transform_c_path = os.path.join(PROJECT_DIR, "lib/transform.c")
    assert os.path.exists(transform_c_path), f"{transform_c_path} is missing."

    with open(transform_c_path, "r") as f:
        content = f.read()

    has_alloc = any(func in content for func in ["malloc", "calloc", "strdup"])
    assert has_alloc, "transform.c does not use dynamic memory allocation (malloc, calloc, or strdup). The memory safety bug is likely not fixed properly."

def test_e2e_script_exists_and_executable():
    """Verify that the end-to-end test script exists and is executable."""
    script_path = os.path.join(PROJECT_DIR, "test_e2e.sh")
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable. Did you forget to run 'chmod +x'?"

def test_e2e_script_execution_and_result():
    """Verify that the end-to-end test script runs successfully and produces the correct output."""
    script_path = os.path.join(PROJECT_DIR, "test_e2e.sh")
    result_path = os.path.join(PROJECT_DIR, "e2e_result.txt")

    # Remove the result file if it exists to ensure the script actually creates it
    if os.path.exists(result_path):
        os.remove(result_path)

    result = subprocess.run(
        [script_path], 
        cwd=PROJECT_DIR, 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"test_e2e.sh failed with exit code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"

    assert os.path.exists(result_path), f"{result_path} was not created by test_e2e.sh."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "HELLOWORLD", f"Expected 'HELLOWORLD' in e2e_result.txt, but got '{content}'."