# test_final_state.py

import os
import subprocess
import time
import pytest

APP_DIR = "/home/user/app"
VENV_DIR = "/home/user/venv"
GATEWAY_SH = os.path.join(APP_DIR, "gateway.sh")
PROCESS_PY = os.path.join(APP_DIR, "process.py")
MAKEFILE = os.path.join(APP_DIR, "Makefile")
HELPER_BIN = os.path.join(APP_DIR, "helper_bin")

def test_venv_and_pyyaml():
    assert os.path.isdir(VENV_DIR), f"Virtual environment directory {VENV_DIR} does not exist."
    python_bin = os.path.join(VENV_DIR, "bin", "python")
    assert os.path.isfile(python_bin), "Python executable not found in the virtual environment."

    # Check if pyyaml is installed
    result = subprocess.run([python_bin, "-c", "import yaml"], capture_output=True)
    assert result.returncode == 0, "pyyaml is not installed in the virtual environment."

def test_makefile_and_compilation():
    assert os.path.isfile(MAKEFILE), f"Makefile {MAKEFILE} does not exist."
    with open(MAKEFILE, "r") as f:
        content = f.read()

    assert "\tgcc" in content, "Makefile should use tabs for indentation, not spaces."
    assert "-lm" in content, "Makefile should include the -lm flag for math library."

    assert os.path.isfile(HELPER_BIN), "helper_bin was not compiled."
    assert os.access(HELPER_BIN, os.X_OK), "helper_bin is not executable."

    result = subprocess.run([HELPER_BIN], capture_output=True, text=True)
    assert result.returncode == 0, "helper_bin failed to execute."
    assert "Helper output: 4" in result.stdout, "helper_bin output is incorrect."

def test_python_script_updated():
    assert os.path.isfile(PROCESS_PY), f"Python script {PROCESS_PY} does not exist."
    with open(PROCESS_PY, "r") as f:
        content = f.read()

    assert "print " not in content, "Python 2 print statements still exist in process.py."
    assert "print(" in content, "Python 3 print() function is not used in process.py."
    assert "yaml.load(" not in content, "Deprecated yaml.load() is still used in process.py."
    assert "yaml.safe_load(" in content, "yaml.safe_load() is not used in process.py."

def test_gateway_sh_executable():
    assert os.path.isfile(GATEWAY_SH), f"Gateway script {GATEWAY_SH} does not exist."
    assert os.access(GATEWAY_SH, os.X_OK), "gateway.sh is not executable."

def test_gateway_403_forbidden():
    env = os.environ.copy()
    env["HTTP_X_API_KEY"] = "wrong_key"
    env["REMOTE_ADDR"] = "10.0.0.1"

    result = subprocess.run([GATEWAY_SH], env=env, capture_output=True, text=True)
    assert "403 Forbidden" in result.stdout, "Gateway did not return '403 Forbidden' for incorrect API key."

def test_gateway_200_ok_and_rate_limit():
    env = os.environ.copy()
    env["HTTP_X_API_KEY"] = "SecretMigrate99"
    env["REMOTE_ADDR"] = "10.0.0.2"

    # First request should succeed
    result1 = subprocess.run([GATEWAY_SH], env=env, capture_output=True, text=True)
    assert "Status: 200 OK" in result1.stdout, "Gateway did not return 'Status: 200 OK' on first valid request."
    assert "Helper output: 4" in result1.stdout, "Gateway did not correctly output the helper_bin result."
    assert "Data: success" in result1.stdout, "Gateway did not correctly output the parsed YAML data."

    # Second request immediately should be rate limited
    result2 = subprocess.run([GATEWAY_SH], env=env, capture_output=True, text=True)
    assert "429 Too Many Requests" in result2.stdout, "Gateway did not return '429 Too Many Requests' on immediate second request."

    # Wait for the rate limit to expire (2 seconds + small buffer)
    time.sleep(2.1)

    # Third request should succeed again
    result3 = subprocess.run([GATEWAY_SH], env=env, capture_output=True, text=True)
    assert "Status: 200 OK" in result3.stdout, "Gateway did not return 'Status: 200 OK' after rate limit expired."