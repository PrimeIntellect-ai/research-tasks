# test_final_state.py
import os
import subprocess
import pytest

def test_ci_vars_env_created():
    path = "/home/user/ci_vars.env"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == 'VERSION="8.7"', f"File {path} does not contain the expected VERSION string. Found: {content}"

def test_app_c_patched():
    path = "/home/user/src/app.c"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "free(arr);" in content, f"File {path} does not appear to be patched. Missing 'free(arr);'."

def test_app_compiled_and_executable():
    path = "/home/user/bin/app"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_app_execution_output():
    path = "/home/user/bin/app"
    assert os.path.isfile(path), f"Executable {path} is missing."
    try:
        result = subprocess.run([path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        expected = "App Version: 8.7"
        assert output == expected, f"Expected output '{expected}', but got '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {path} failed with return code {e.returncode}")