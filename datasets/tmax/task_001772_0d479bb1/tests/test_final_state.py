# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/test_env"

def test_result_log_exists():
    result_path = os.path.join(BASE_DIR, "result.log")
    assert os.path.exists(result_path), f"{result_path} does not exist. The runner output was not saved."
    assert os.path.isfile(result_path), f"{result_path} is not a file."

def test_result_log_content():
    result_path = os.path.join(BASE_DIR, "result.log")
    assert os.path.exists(result_path), "Cannot check content, result.log is missing."
    with open(result_path, "r") as f:
        content = f.read().strip()

    # Based on data.txt (15+25+40+20+100 = 200)
    expected = "Data sum: 200"
    assert content == expected, f"Expected '{expected}' in result.log, but got '{content}'."

def test_build_artifacts_exist():
    lib_path = os.path.join(BASE_DIR, "lib", "libdata.so")
    bin_path = os.path.join(BASE_DIR, "bin", "runner")

    assert os.path.exists(lib_path), f"Shared library {lib_path} was not built."
    assert os.path.exists(bin_path), f"Executable {bin_path} was not built."

def test_abi_fix_in_header():
    header_path = os.path.join(BASE_DIR, "include", "libdata.h")
    assert os.path.exists(header_path), f"{header_path} is missing."

    with open(header_path, "r") as f:
        content = f.read()

    assert 'extern "C"' in content, "The ABI linkage issue was not fixed. Expected 'extern \"C\"' in libdata.h."

def test_makefile_fpic_fix():
    makefile_path = os.path.join(BASE_DIR, "Makefile")
    assert os.path.exists(makefile_path), f"{makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-fPIC" in content, "The Makefile does not contain '-fPIC' for compiling the shared library."