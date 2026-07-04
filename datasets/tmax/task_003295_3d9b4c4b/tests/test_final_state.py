# test_final_state.py
import os
import re
import subprocess
import pytest

WORKDIR = "/home/user/polyglot-data"

def test_makefile_builds_successfully():
    """Verify that running make succeeds without errors."""
    result = subprocess.run(["make", "-C", WORKDIR], capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}"

def test_libprocessor_so_exists():
    """Verify that the shared library was built."""
    so_path = os.path.join(WORKDIR, "libprocessor.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

def test_app_exists_and_links_dynamically():
    """Verify that the executable was built and dynamically links to libprocessor.so."""
    app_path = os.path.join(WORKDIR, "app")
    assert os.path.isfile(app_path), f"Executable {app_path} was not built."

    result = subprocess.run(["ldd", app_path], capture_output=True, text=True)
    assert result.returncode == 0, f"ldd failed on {app_path}"
    assert "libprocessor.so" in result.stdout, f"{app_path} does not dynamically link to libprocessor.so"

def test_test_script_exists():
    """Verify that the test.sh script exists."""
    script_path = os.path.join(WORKDIR, "test.sh")
    assert os.path.isfile(script_path), f"Test script {script_path} does not exist."

def test_output_log_format():
    """Verify that output.log exists, has exactly 10 lines, and matches the correct format."""
    log_path = os.path.join(WORKDIR, "output.log")
    assert os.path.isfile(log_path), f"Output log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 lines in {log_path}, found {len(lines)}."

    pattern = re.compile(r"^id:\d+,value:\d+$")
    for i, line in enumerate(lines):
        assert pattern.match(line), f"Line {i+1} in {log_path} does not match the expected format: '{line}'"