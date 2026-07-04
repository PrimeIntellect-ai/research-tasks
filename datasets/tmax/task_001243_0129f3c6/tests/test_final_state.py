# test_final_state.py

import os
import stat
import pytest

def test_run_mc_script_exists_and_executable():
    script_path = "/home/user/run_mc.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_inv_executable_exists():
    exe_path = "/home/user/inv"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist. Did the script compile it?"
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled file {exe_path} is not executable."

def test_result_file_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "0.001", f"Expected result file to contain '0.001', but found '{content}'"