# test_final_state.py

import os
import pytest

def test_libprocessor_so_exists():
    path = "/home/user/project/libprocessor.so"
    assert os.path.isfile(path), f"Shared library {path} is missing. Did you compile the C code?"

def test_integration_py_exists_and_uses_ctypes():
    path = "/home/user/project/integration.py"
    assert os.path.isfile(path), f"Python script {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "ctypes" in content, f"{path} does not seem to use the 'ctypes' module as required."

def test_result_log_content():
    path = "/home/user/result.log"
    assert os.path.isfile(path), f"Result log file {path} is missing. Did the integration script run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_output = "ZYX_DAOLYAP_GNOL_11224488_ESNOPSER_NEKOT"
    assert content == expected_output, f"Content of {path} is incorrect. Expected '{expected_output}', but got '{content}'."