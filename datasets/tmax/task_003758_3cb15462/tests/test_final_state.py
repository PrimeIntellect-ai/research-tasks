# test_final_state.py
import os
import hashlib

def test_keygen_cpp_exists():
    path = "/home/user/keygen.cpp"
    assert os.path.isfile(path), f"File {path} does not exist. You need to write the C++ program."

def test_keygen_executable_exists():
    path = "/home/user/keygen"
    assert os.path.isfile(path), f"Executable {path} does not exist. You need to compile the C++ program."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_new_token_correct():
    path = "/home/user/new_token.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The program must generate it."

    password = "StrictPassword2024!"
    salt = "8xK#mP9vLq2$zR5w"
    combined = password + salt
    expected_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    expected_token = f"AUTH-TOKEN-{expected_hash}"

    with open(path, "r") as f:
        content = f.read()

    assert content == expected_token, f"The contents of {path} are incorrect. Expected '{expected_token}', but got '{content}'."