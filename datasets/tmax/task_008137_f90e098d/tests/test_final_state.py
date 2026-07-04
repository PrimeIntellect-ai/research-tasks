# test_final_state.py

import os

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"

    assert os.path.exists(flag_path), f"The file {flag_path} does not exist. The script might not have run correctly or saved to the wrong location."

    with open(flag_path, "r") as f:
        flag_content = f.read().strip()

    expected_flag = "SEC_99x_DEADLOCK"
    assert flag_content == expected_flag, f"Incorrect flag. Expected '{expected_flag}', but got '{flag_content}'."

def test_mem_dump_exists():
    dump_path = "/home/user/workspace/mem.dmp"
    assert os.path.exists(dump_path), f"The memory dump {dump_path} does not exist. Did you run the compiled decrypt_tool?"

def test_binary_exists():
    binary_path = "/home/user/workspace/decrypt_tool"
    assert os.path.exists(binary_path), f"The compiled binary {binary_path} does not exist. Did you successfully compile the C program?"