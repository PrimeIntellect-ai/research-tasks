# test_final_state.py
import os

def test_key_txt_content():
    key_path = "/home/user/key.txt"
    assert os.path.exists(key_path), f"File {key_path} does not exist. The task requires saving the key to this file."
    assert os.path.isfile(key_path), f"{key_path} is not a file."

    with open(key_path, "r") as f:
        content = f.read().strip()

    assert content == "10001.00000", f"Expected key to be '10001.00000', but got '{content}'."