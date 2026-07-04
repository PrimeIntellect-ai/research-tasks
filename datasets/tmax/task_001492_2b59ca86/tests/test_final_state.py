# test_final_state.py
import os

def test_exploit_source_exists():
    path = "/home/user/exploit.cpp"
    assert os.path.isfile(path), f"Exploit source code is missing. Expected to find it at {path}."

def test_exploit_binary_exists_and_executable():
    path = "/home/user/exploit"
    assert os.path.isfile(path), f"Compiled exploit binary is missing. Expected to find it at {path}."
    assert os.access(path, os.X_OK), f"The compiled exploit at {path} is not executable."

def test_flag_file_contents():
    path = "/home/user/flag.txt"
    assert os.path.isfile(path), f"Flag file is missing. Expected to find it at {path}."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{alg_none_priv_esc_successful}"
    assert content == expected_flag, f"Flag file content is incorrect. Expected '{expected_flag}', but got '{content}'."