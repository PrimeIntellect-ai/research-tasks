# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

def test_libsec_so_exists_and_valid():
    lib_path = "/home/user/app/libsec.so"
    assert os.path.isfile(lib_path), f"{lib_path} does not exist. Did you run the fixed build.sh?"

    # Check if it's a valid shared object by running ldd or file
    # file command is safer to check if it's a shared object
    result = subprocess.run(["file", lib_path], capture_output=True, text=True)
    assert "shared object" in result.stdout, f"{lib_path} is not a valid shared object."

def test_rest_api_sh_exists_and_executable():
    script_path = "/home/user/app/rest_api.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_rest_api_sh_valid_token():
    script_path = "/home/user/app/rest_api.sh"
    result = subprocess.run([script_path, "A123"], capture_output=True, text=True)

    output = result.stdout.strip()
    expected = '{"endpoint": "/api/validate", "token_valid": true}'
    assert output == expected, f"Expected output '{expected}' for valid token, but got '{output}'"

def test_rest_api_sh_invalid_token():
    script_path = "/home/user/app/rest_api.sh"
    result = subprocess.run([script_path, "B123"], capture_output=True, text=True)

    output = result.stdout.strip()
    expected = '{"endpoint": "/api/validate", "token_valid": false}'
    assert output == expected, f"Expected output '{expected}' for invalid token, but got '{output}'"