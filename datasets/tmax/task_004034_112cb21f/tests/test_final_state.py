# test_final_state.py
import os
import subprocess
import pytest

def test_build_output_exists_and_correct():
    output_path = "/home/user/tool/build/output.txt"
    assert os.path.isfile(output_path), f"Verification file {output_path} does not exist. The script may not have run main.py successfully."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "SUCCESS_420", f"Expected output.txt to contain 'SUCCESS_420', but got '{content}'"

def test_shared_library_compiled():
    lib_path = "/home/user/tool/build/libalgo.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Compilation step failed."

def test_virtual_environment_created():
    venv_python = "/home/user/tool/venv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment Python executable {venv_python} does not exist."
    assert os.access(venv_python, os.X_OK), f"{venv_python} is not executable."

def test_requirements_installed_in_venv():
    venv_python = "/home/user/tool/venv/bin/python"
    # Execute a simple import to verify requests is installed in the venv
    try:
        result = subprocess.run(
            [venv_python, "-c", "import requests; print(requests.__version__)"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "2.31.0" in result.stdout, f"Expected requests version 2.31.0, got {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import 'requests' in the virtual environment. Error: {e.stderr}")

def test_ci_build_script_exists():
    script_path = "/home/user/tool/ci_build.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."