# test_final_state.py
import os
import subprocess
import pytest

def test_test_results_log():
    log_path = "/home/user/project/test_results.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Did you run the client and redirect output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "FeatureData-778899" in content, f"Expected 'FeatureData-778899' in {log_path}, but got: {content}"

def test_rust_server_compiles():
    rust_dir = "/home/user/project/backend_rust"
    assert os.path.isdir(rust_dir), f"Directory {rust_dir} does not exist."

    # Verify that the rust code compiles successfully now
    result = subprocess.run(["cargo", "check"], cwd=rust_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Rust server still does not compile. Cargo check failed:\n{result.stderr}"

def test_cpp_client_compiles():
    exe_path = "/home/user/project/client_cpp/build/feature_test"
    assert os.path.exists(exe_path), f"Compiled C++ client {exe_path} does not exist. Did you build it?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_cmake_fixed():
    cmake_path = "/home/user/project/client_cpp/CMakeLists.txt"
    assert os.path.exists(cmake_path), f"{cmake_path} is missing."

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "target_link_libraries" in content, "CMakeLists.txt is still missing target_link_libraries. The C++ client won't link successfully without it."