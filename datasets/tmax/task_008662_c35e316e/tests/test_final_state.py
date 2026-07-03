# test_final_state.py

import os
import pytest

def test_polybuild_script_exists():
    script_path = "/home/user/polybuild/polybuild.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_shared_library_compiled():
    lib_path = "/home/user/polybuild/libop_lib.so"
    assert os.path.isfile(lib_path), f"Expected compiled shared library {lib_path} does not exist."

def test_result_out_content():
    result_path = "/home/user/polybuild/result.out"
    assert os.path.isfile(result_path), f"Expected output file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "176", f"Expected result.out to contain '176', but got '{content}'."