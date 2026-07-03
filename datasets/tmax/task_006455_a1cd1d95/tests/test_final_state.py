# test_final_state.py

import os
import json
import subprocess
import pytest

def test_resolved_versions_json():
    """Verify that resolved_versions.json exists and has the correct exact versions."""
    filepath = "/home/user/resolved_versions.json"
    assert os.path.exists(filepath), f"File {filepath} is missing."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} is not a valid JSON.")

    expected_data = {
        "test-runner": "1.0.0",
        "lib-gamma": "1.0.0",
        "lib-beta": "2.0.0",
        "lib-alpha": "1.1.0"
    }

    assert data == expected_data, f"Content of {filepath} does not match expected resolved versions. Got {data}"

def test_source_files_exist():
    """Verify that the generated source files exist."""
    src_files = [
        "/home/user/src/lib-alpha.c",
        "/home/user/src/lib-beta.c",
        "/home/user/src/lib-gamma.c",
        "/home/user/src/main.c"
    ]
    for f in src_files:
        assert os.path.exists(f), f"Source file {f} is missing."

def test_compiled_shared_objects_exist():
    """Verify that the compiled shared objects exist with the correct versioned names."""
    so_files = [
        "/home/user/build/lib-alpha-1.1.0.so",
        "/home/user/build/lib-beta-2.0.0.so",
        "/home/user/build/lib-gamma-1.0.0.so"
    ]
    for f in so_files:
        assert os.path.exists(f), f"Shared object file {f} is missing."

def test_executable_exists_and_runs():
    """Verify that test-runner exists, is executable, and runs without errors."""
    exe_path = "/home/user/build/test-runner"
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    # Run the executable, providing LD_LIBRARY_PATH in case rpath wasn't set.
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/build" + (":" + env["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in env else "")

    try:
        result = subprocess.run([exe_path], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        assert result.returncode == 0, f"Running {exe_path} failed with exit code {result.returncode}. Stderr: {result.stderr.decode()}"
    except Exception as e:
        pytest.fail(f"Failed to execute {exe_path}: {e}")

def test_executable_dynamic_linking():
    """Verify that test-runner is dynamically linked against the correct versioned shared objects."""
    exe_path = "/home/user/build/test-runner"
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing."

    try:
        result = subprocess.run(["ldd", exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        ldd_output = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ldd command failed on {exe_path}: {e.stderr}")

    expected_libs = [
        "lib-alpha-1.1.0.so",
        "lib-beta-2.0.0.so",
        "lib-gamma-1.0.0.so"
    ]

    for lib in expected_libs:
        assert lib in ldd_output, f"Executable is not dynamically linked against {lib}. ldd output:\n{ldd_output}"