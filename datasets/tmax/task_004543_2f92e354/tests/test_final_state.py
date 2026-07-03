# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = '/home/user/fix_and_build.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_shared_library_exists():
    lib_path = '/home/user/project/lib/libmathops.so'
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist."

def test_executable_exists_and_executable():
    app_path = '/home/user/project/calc_app'
    assert os.path.isfile(app_path), f"Executable {app_path} does not exist."
    assert os.access(app_path, os.X_OK), f"Executable {app_path} is not executable."

def test_result_file_correct():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you run your script?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "70", f"Expected result to be '70', but got '{content}'."