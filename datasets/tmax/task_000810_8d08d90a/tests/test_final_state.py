# test_final_state.py
import os
import pytest

def test_flag_txt_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Missing file: {flag_path}"

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{pr0c_cmdl1n3_l34k5_4r3_f4t4l}"
    assert content == expected_flag, f"Incorrect flag content in {flag_path}. Expected '{expected_flag}', got '{content}'"

def test_exploit_script_exists():
    exploit_py = "/home/user/exploit.py"
    exploit_sh = "/home/user/exploit.sh"

    assert os.path.isfile(exploit_py) or os.path.isfile(exploit_sh), (
        f"Exploit script missing. Expected either {exploit_py} or {exploit_sh} to exist."
    )