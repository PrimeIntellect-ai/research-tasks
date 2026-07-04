# test_final_state.py

import os
import pytest

def test_calc_kl_script_exists_and_executable():
    script_path = "/home/user/calc_kl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_find_root_script_exists_and_executable():
    script_path = "/home/user/find_root.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_kl_out_content():
    out_path = "/home/user/kl_out.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    with open(out_path, "r") as f:
        content = f.read().strip()

    assert content == "0.05754", f"Expected KL divergence output to be '0.05754', got '{content}'."

def test_root_out_content():
    out_path = "/home/user/root_out.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    with open(out_path, "r") as f:
        content = f.read().strip()

    assert content == "1.02829", f"Expected root output to be '1.02829', got '{content}'."