# test_final_state.py
import os

def test_decrypted_secret():
    path = "/home/user/decrypted_secret.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    expected = "OPERATION_MIDNIGHT_ECLIPSE"
    assert content == expected, f"File {path} content is incorrect. Expected '{expected}', got '{content}'."