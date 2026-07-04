# test_final_state.py

import os
import subprocess
import pytest

API_KEY_FILE = "/home/user/api_key.txt"
PROJECT_DIR = "/home/user/project"
BUILD_SCRIPT = os.path.join(PROJECT_DIR, "build.sh")
MRE_SCRIPT = os.path.join(PROJECT_DIR, "mre.sh")
EXPECTED_API_KEY = "xk93_Lz91_deploy_secret_99"

def test_api_key_extracted_correctly():
    assert os.path.isfile(API_KEY_FILE), f"API key file not found at {API_KEY_FILE}"

    with open(API_KEY_FILE, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_API_KEY, f"API key file content is incorrect. Expected '{EXPECTED_API_KEY}', got '{content}'"

def test_build_script_succeeds():
    assert os.path.isfile(BUILD_SCRIPT), f"Build script not found at {BUILD_SCRIPT}"
    assert os.access(BUILD_SCRIPT, os.X_OK), f"Build script at {BUILD_SCRIPT} is not executable"

    result = subprocess.run([BUILD_SCRIPT], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Build script failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_mre_script_exists_and_executable():
    assert os.path.isfile(MRE_SCRIPT), f"MRE script not found at {MRE_SCRIPT}"
    assert os.access(MRE_SCRIPT, os.X_OK), f"MRE script at {MRE_SCRIPT} is not executable"

def test_mre_script_functionality():
    test_input = "3.14159 # pi"
    expected_output = "3.14159"

    result = subprocess.run([MRE_SCRIPT, test_input], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"MRE script failed with exit code {result.returncode}.\nSTDERR:\n{result.stderr}"

    output = result.stdout.strip()
    assert output == expected_output, f"MRE script output is incorrect. Expected '{expected_output}', got '{output}'"

def test_mre_script_functionality_no_comment():
    test_input = "2.718"
    expected_output = "2.718"

    result = subprocess.run([MRE_SCRIPT, test_input], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"MRE script failed with exit code {result.returncode}.\nSTDERR:\n{result.stderr}"

    output = result.stdout.strip()
    assert output == expected_output, f"MRE script output is incorrect. Expected '{expected_output}', got '{output}'"