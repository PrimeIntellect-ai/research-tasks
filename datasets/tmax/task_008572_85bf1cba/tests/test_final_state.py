# test_final_state.py
import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
BUILD_SH = os.path.join(PROJECT_DIR, "build.sh")
TEST_BUILD_SH = os.path.join(PROJECT_DIR, "test_build.sh")
APP = os.path.join(PROJECT_DIR, "app")

def test_test_build_sh_exists_and_executable():
    assert os.path.isfile(TEST_BUILD_SH), f"File {TEST_BUILD_SH} is missing."
    assert os.access(TEST_BUILD_SH, os.X_OK), f"File {TEST_BUILD_SH} is not executable."

def test_test_build_sh_execution():
    # Clean up app if it exists to ensure test_build.sh actually builds it or relies on build.sh
    if os.path.exists(APP):
        os.remove(APP)

    result = subprocess.run(
        [TEST_BUILD_SH],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"{TEST_BUILD_SH} failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_app_exists_and_executable():
    assert os.path.isfile(APP), f"Executable {APP} is missing. The build script might not have produced it."
    assert os.access(APP, os.X_OK), f"File {APP} is not executable."

def test_app_output():
    # Run the app and check the output
    result = subprocess.run(
        [APP],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"{APP} failed to run with exit code {result.returncode}."
    assert "Build success!" in result.stdout, f"Expected 'Build success!' in output, but got: {result.stdout}"
    assert "Utils module loaded." in result.stdout, f"Expected 'Utils module loaded.' in output, but got: {result.stdout}"

def test_build_sh_fixed():
    # Ensure build.sh actually links utils.o or compiles correctly
    with open(BUILD_SH, "r") as f:
        content = f.read()
    # It should mention utils.o or utils.c in the gcc command that produces app
    assert "gcc" in content and "app" in content, f"{BUILD_SH} does not seem to compile 'app' anymore."