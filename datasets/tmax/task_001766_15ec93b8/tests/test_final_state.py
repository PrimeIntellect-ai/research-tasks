# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist():
    """Check that the required source and build files exist."""
    required_files = [
        "/home/user/solver.cpp",
        "/home/user/Makefile",
        "/home/user/libsolver.so",
        "/home/user/app"
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file {file_path} is missing."

def test_output_txt():
    """Check that output.txt contains the correct validation results."""
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"File {output_path} is missing. Did the app run successfully?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected = "TEST1: VALID\nTEST2: CORRECT_NO_SOLUTION"
    assert content == expected, f"Output file content is incorrect.\nExpected:\n{expected}\n\nGot:\n{content}"

def test_dynamic_linking_and_rpath():
    """Check that the app is dynamically linked to libsolver.so and has an RPATH/RUNPATH."""
    app_path = "/home/user/app"
    assert os.path.isfile(app_path), f"Executable {app_path} is missing."

    try:
        result = subprocess.run(["readelf", "-d", app_path], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        pytest.fail("readelf command not found. Cannot verify dynamic linking.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run readelf on app. Error: {e.stderr}")

    output = result.stdout

    # Check for dynamic dependency on libsolver.so
    assert "libsolver.so" in output, "The executable 'app' is not dynamically linked to 'libsolver.so'."

    # Check for RPATH or RUNPATH pointing to the current directory (., /home/user, or $ORIGIN)
    has_valid_rpath = False
    for line in output.splitlines():
        if "(RPATH)" in line or "(RUNPATH)" in line:
            # The path is usually enclosed in brackets, e.g., Library rpath: [.]
            if "." in line or "/home/user" in line or "$ORIGIN" in line:
                has_valid_rpath = True
                break

    assert has_valid_rpath, (
        "The executable 'app' does not have a valid RPATH or RUNPATH pointing to "
        "the current directory (e.g., '.', '/home/user', or '$ORIGIN').\n"
        f"readelf output:\n{output}"
    )

def test_app_execution_succeeds():
    """Check that the app can be executed without LD_LIBRARY_PATH and returns 0."""
    app_path = "/home/user/app"

    # Create an environment explicitly without LD_LIBRARY_PATH
    env = os.environ.copy()
    env.pop("LD_LIBRARY_PATH", None)

    try:
        result = subprocess.run([app_path], env=env, cwd="/home/user", capture_output=True, text=True)
        assert result.returncode == 0, f"Running {app_path} failed with return code {result.returncode}.\nStderr: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to execute {app_path}: {e}")