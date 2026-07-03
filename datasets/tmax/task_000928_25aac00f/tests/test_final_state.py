# test_final_state.py

import os
import subprocess
import pytest

def test_auth_cpp_exists_and_fixed():
    path = "/home/user/auth.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "// AUTH_MODULE_START" in content, "auth.cpp is missing the start marker."
    assert "namespace Auth" in content, "auth.cpp does not contain the corrected 'namespace Auth'."
    assert "namespace Authentication" not in content, "auth.cpp still contains the incorrect 'namespace Authentication'."

def test_libauth_so_exists_and_exports_symbol():
    path = "/home/user/libauth.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist."

    # Check if the correct symbol is exported
    try:
        output = subprocess.check_output(["nm", "-D", path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    except FileNotFoundError:
        # Fallback to readelf if nm is not available
        output = subprocess.check_output(["readelf", "-s", path], text=True)

    assert "_ZN4Auth12verify_tokenEiPKc" in output, f"Library {path} does not export the required symbol '_ZN4Auth12verify_tokenEiPKc'."

def test_reproduce_sh_exists_and_valid():
    path = "/home/user/reproduce.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "auth_service" in content, "reproduce.sh does not seem to execute auth_service."
    assert "status.log" in content, "reproduce.sh does not reference status.log."
    assert "CRASHED" in content, "reproduce.sh does not contain the word 'CRASHED'."

def test_status_log_contains_crashed():
    path = "/home/user/status.log"
    assert os.path.isfile(path), f"Log file {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "CRASHED" in content, f"Log file {path} does not contain the word 'CRASHED'."