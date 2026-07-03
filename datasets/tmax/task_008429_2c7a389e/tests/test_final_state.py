# test_final_state.py

import os
import base64
import stat
import pytest

def test_test_sh_exists_and_executable():
    path = "/home/user/test.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_wrapper_binary_exists_and_executable():
    path = "/home/user/crypto-wrapper/wrapper"
    assert os.path.isfile(path), f"Binary {path} is missing. Did test.sh build the Go application?"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_main_go_fixed():
    path = "/home/user/crypto-wrapper/main.go"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "LDFLAGS" in content and "-lcrypto" in content, "main.go does not seem to have the correct #cgo LDFLAGS directive."

def test_final_txt_exists_and_correct():
    path = "/home/user/final.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did test.sh generate it?"

    with open(path, "r") as f:
        encoded_content = f.read().strip()

    try:
        decoded_bytes = base64.b64decode(encoded_content)
        decoded_str = decoded_bytes.decode('utf-8', errors='replace')
    except Exception as e:
        pytest.fail(f"Failed to decode base64 content in {path}: {e}")

    expected_substring = "UryybJroFrphevgl:3948574326"
    assert expected_substring in decoded_str, f"Decoded content does not contain the expected output. Got: {decoded_str}"