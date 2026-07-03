# test_final_state.py

import os
import re
import stat
import pytest

def test_proto_file_exists_and_content():
    """Verify that telemetry.proto exists and contains the required definitions."""
    proto_path = "/home/user/project/telemetry.proto"
    assert os.path.isfile(proto_path), f"Missing protobuf file: {proto_path}"

    with open(proto_path, "r") as f:
        content = f.read()

    assert "package telemetry;" in content or "package telemetry" in content, "Missing 'telemetry' package in proto file"
    assert "service TelemetryService" in content, "Missing 'TelemetryService' in proto file"
    assert "rpc StreamMetrics" in content, "Missing 'StreamMetrics' RPC in proto file"
    assert "message Metric" in content, "Missing 'Metric' message in proto file"

def test_cpp_bridge_file_exists():
    """Verify that bridge.cpp exists."""
    cpp_path = "/home/user/project/bridge.cpp"
    assert os.path.isfile(cpp_path), f"Missing C++ source file: {cpp_path}"

def test_cmake_lists_exists():
    """Verify that CMakeLists.txt exists."""
    cmake_path = "/home/user/project/CMakeLists.txt"
    assert os.path.isfile(cmake_path), f"Missing CMakeLists.txt: {cmake_path}"

def test_build_and_package_script_exists_and_executable():
    """Verify that build_and_package.sh exists and is executable."""
    script_path = "/home/user/project/build_and_package.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {script_path}"

def test_dist_bin_contains_executable():
    """Verify that the packaging script created the dist bin directory and the executable."""
    bin_dir = "/home/user/dist/bin"
    assert os.path.isdir(bin_dir), f"Missing dist bin directory: {bin_dir}"

    exe_path = os.path.join(bin_dir, "telemetry_bridge")
    assert os.path.isfile(exe_path), f"Missing executable in dist: {exe_path}"

    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Packaged binary is not executable: {exe_path}"

def test_dist_lib_contains_libraries():
    """Verify that the packaging script copied dynamic libraries into dist lib."""
    lib_dir = "/home/user/dist/lib"
    assert os.path.isdir(lib_dir), f"Missing dist lib directory: {lib_dir}"

    libs = [f for f in os.listdir(lib_dir) if os.path.isfile(os.path.join(lib_dir, f))]
    assert len(libs) >= 3, f"Expected multiple shared libraries packaged in {lib_dir}, found {len(libs)}"