# test_final_state.py

import os
import stat
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_build_script_exists_and_executable():
    script_path = os.path.join(PROJECT_DIR, "build_and_run.sh")
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_libalgo_exists():
    lib_path = os.path.join(PROJECT_DIR, "libalgo.so")
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not built or is missing."

def test_math_runner_exists():
    binary_path = os.path.join(PROJECT_DIR, "math_runner")
    assert os.path.isfile(binary_path), f"Executable {binary_path} was not built or is missing."

    st = os.stat(binary_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Executable {binary_path} does not have execute permissions."

def test_math_runner_rpath():
    binary_path = os.path.join(PROJECT_DIR, "math_runner")
    assert os.path.isfile(binary_path), "Cannot check rpath because math_runner is missing."

    result = subprocess.run(["readelf", "-d", binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run readelf on {binary_path}."

    rpath_found = False
    for line in result.stdout.splitlines():
        if "RPATH" in line or "RUNPATH" in line:
            # Check if the rpath points to the current directory, project directory, or uses $ORIGIN
            if "." in line or PROJECT_DIR in line or "$ORIGIN" in line:
                rpath_found = True
                break

    assert rpath_found, f"{binary_path} does not have a valid RPATH/RUNPATH set to find libalgo.so."

def test_output_log_correct():
    log_path = os.path.join(PROJECT_DIR, "output.log")
    assert os.path.isfile(log_path), f"Output log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    # The sum of 1 to 15 is 120. Protobuf ShortDebugString format typically looks like "limit: 15 result: 120"
    assert "limit: 15" in content, f"output.log does not contain 'limit: 15'. Content: {content}"
    assert "result: 120" in content, f"output.log does not contain 'result: 120'. Content: {content}"

def test_math_runner_execution_without_ld_library_path():
    binary_path = os.path.join(PROJECT_DIR, "math_runner")
    assert os.path.isfile(binary_path), "Cannot test execution because math_runner is missing."

    # Run the binary from the project directory without setting LD_LIBRARY_PATH
    # to ensure rpath is actually working.
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        del env["LD_LIBRARY_PATH"]

    try:
        result = subprocess.run(
            [binary_path, "math://service/compute?limit=5"],
            cwd=PROJECT_DIR,
            env=env,
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0, f"math_runner failed to execute. Error: {result.stderr}"
        assert "limit: 5" in result.stdout and "result: 15" in result.stdout, "math_runner did not produce expected output for limit=5."
    except Exception as e:
        pytest.fail(f"Execution of math_runner failed: {e}")