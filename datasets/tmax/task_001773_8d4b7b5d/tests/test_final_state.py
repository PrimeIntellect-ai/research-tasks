# test_final_state.py

import os
import pytest

def test_pi_result_exists_and_correct():
    result_path = "/home/user/pi_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing. The script did not run successfully or did not produce the expected output file."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "3.1424", f"Expected pi_result.txt to contain exactly '3.1424', but got '{content}'."

def test_calc_pi_sh_fixed_and_executable():
    script_path = "/home/user/calc_pi.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_helper_compiled():
    binary_path = "/home/user/term_calc"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing. The gcc compilation step failed."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."