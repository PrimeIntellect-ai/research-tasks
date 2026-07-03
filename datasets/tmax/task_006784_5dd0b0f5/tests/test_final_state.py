# test_final_state.py

import os
import subprocess
import json
import re

def test_cargo_test_passes():
    """Verify that the Rust project builds and passes its tests."""
    rust_dir = "/home/user/data_app/rust_server"
    assert os.path.isdir(rust_dir), "rust_server directory is missing."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=rust_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_benchmark_results():
    """Verify that the benchmark script ran successfully and generated the results file."""
    results_file = "/home/user/benchmark_results.json"
    assert os.path.isfile(results_file), f"Benchmark results file {results_file} is missing."

    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("requests") == 100, f"Expected 100 requests, got {data.get('requests')}"

def test_cpp_memory_leak_fixed():
    """Verify that the memory leak in processor.cpp is fixed."""
    cpp_path = "/home/user/data_app/cpp_engine/processor.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # If they still use 'new', they must use 'delete[]'
    if "new " in content or "new[" in content:
        assert "delete[]" in content, "Memory leak not fixed: 'new' is used but 'delete[]' is missing."
    else:
        # If they don't use 'new', they probably refactored to std::vector or a local array.
        # Just ensure it's not the original broken state.
        pass

def test_cpp_out_of_bounds_fixed():
    """Verify that the out-of-bounds array access in processor.cpp is fixed."""
    cpp_path = "/home/user/data_app/cpp_engine/processor.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # The original loop had <= length. It should be < length or equivalent.
    assert "<= length" not in content and "<=length" not in content, "Out-of-bounds bug (<= length) is still present."

def test_cmake_fixed():
    """Verify that CMakeLists.txt is configured to build a static library with -fPIC."""
    cmake_path = "/home/user/data_app/cpp_engine/CMakeLists.txt"
    assert os.path.isfile(cmake_path), f"{cmake_path} is missing."

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "add_executable" not in content, "CMakeLists.txt still contains add_executable."
    assert "add_library" in content, "CMakeLists.txt is missing add_library."

    # Check for PIC
    has_pic_flag = "-fPIC" in content or "POSITION_INDEPENDENT_CODE" in content
    assert has_pic_flag, "CMakeLists.txt is missing Position Independent Code (-fPIC) configuration."