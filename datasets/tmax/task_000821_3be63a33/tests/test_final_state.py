# test_final_state.py

import os
import re
import ctypes
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
OUTPUT_LOG = "/home/user/output.log"
EXPECTED_HEX = "506F6C79676C6F7444617461313233"

def test_output_log_correct():
    assert os.path.isfile(OUTPUT_LOG), f"{OUTPUT_LOG} does not exist."
    with open(OUTPUT_LOG, "r") as f:
        content = f.read().strip()

    assert EXPECTED_HEX.lower() in content.lower(), f"Expected hex string {EXPECTED_HEX} not found in {OUTPUT_LOG}."

def test_shared_objects_exist():
    libencoder_so = os.path.join(PROJECT_DIR, "libencoder.so")
    wrapper_so = os.path.join(PROJECT_DIR, "wrapper.so")

    assert os.path.isfile(libencoder_so), f"{libencoder_so} does not exist."
    assert os.path.isfile(wrapper_so), f"{wrapper_so} does not exist."

    # Check that they are actually shared objects
    out_lib = subprocess.check_output(["file", libencoder_so]).decode("utf-8")
    assert "shared object" in out_lib, f"{libencoder_so} is not a valid shared object."

    out_wrap = subprocess.check_output(["file", wrapper_so]).decode("utf-8")
    assert "shared object" in out_wrap, f"{wrapper_so} is not a valid shared object."

def test_c_code_memory_fix():
    libencoder_c = os.path.join(PROJECT_DIR, "libencoder.c")
    assert os.path.isfile(libencoder_c), f"{libencoder_c} does not exist."

    with open(libencoder_c, "r") as f:
        content = f.read()

    # Check that the original buggy malloc(len * 2) is gone or fixed
    # A correct fix would be malloc(len * 2 + 1), calloc, or similar
    bug_pattern = re.compile(r"malloc\s*\(\s*len\s*\*\s*2\s*\)")

    # If the exact bug pattern is found, check if there's a +1 or + 1 somewhere in the same line
    lines = content.split('\n')
    for line in lines:
        if bug_pattern.search(line):
            assert "+1" in line.replace(" ", "") or "calloc" in line, \
                "libencoder.c still seems to contain the memory allocation bug (allocating exactly len * 2 without +1)."

def test_ws_server_script_exists():
    ws_server = os.path.join(PROJECT_DIR, "ws_server.py")
    assert os.path.isfile(ws_server), f"{ws_server} does not exist."

    with open(ws_server, "r") as f:
        content = f.read()

    assert "websockets" in content, "ws_server.py does not seem to use the 'websockets' library."
    assert "ctypes" in content, "ws_server.py does not seem to use the 'ctypes' library."

def test_wrapper_functionality():
    wrapper_so = os.path.join(PROJECT_DIR, "wrapper.so")
    assert os.path.isfile(wrapper_so), "wrapper.so missing, cannot test functionality."

    # Try to load the wrapper and call encode_string
    try:
        wrapper = ctypes.CDLL(wrapper_so)
        wrapper.encode_string.argtypes = [ctypes.c_char_p]
        wrapper.encode_string.restype = ctypes.c_char_p

        test_str = b"Test"
        result = wrapper.encode_string(test_str)
        assert result.decode('utf-8').upper() == "54657374", "encode_string did not return the correct hex string."
    except Exception as e:
        pytest.fail(f"Failed to load wrapper.so or call encode_string: {e}")