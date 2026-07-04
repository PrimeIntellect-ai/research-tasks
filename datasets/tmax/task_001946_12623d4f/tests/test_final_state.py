# test_final_state.py

import os
import subprocess
import pytest

def test_key_recovered():
    key_path = "/home/user/investigation/key.txt"
    assert os.path.isfile(key_path), f"The file {key_path} does not exist."
    with open(key_path, "r") as f:
        key = f.read().strip()
    assert key == "secret", "The recovered key in key.txt is incorrect."

def test_forged_token():
    token_path = "/home/user/investigation/forged_token.txt"
    assert os.path.isfile(token_path), f"The file {token_path} does not exist."

    # Compute the expected token dynamically
    username = "system_admin"
    key = "secret"
    expected_token = "".join(f"{ord(c) ^ ord(key[i % len(key)]):02x}" for i, c in enumerate(username))

    with open(token_path, "r") as f:
        token = f.read().strip().lower()

    assert token == expected_token, f"The forged token in {token_path} is incorrect."

def test_injection_payload():
    payload_path = "/home/user/investigation/payload.txt"
    source_path = "/home/user/investigation/auth_service.cpp"
    bin_path = "/home/user/investigation/auth_service"
    pwned_path = "/home/user/investigation/pwned"

    assert os.path.isfile(payload_path), f"The file {payload_path} does not exist."

    with open(payload_path, "r") as f:
        payload = f.read().strip()

    # Compile the vulnerable program if it hasn't been compiled
    if not os.path.isfile(bin_path):
        compile_proc = subprocess.run(["g++", source_path, "-o", bin_path], capture_output=True)
        assert compile_proc.returncode == 0, "Failed to compile auth_service.cpp."

    # Ensure the pwned file does not exist before testing
    if os.path.exists(pwned_path):
        os.remove(pwned_path)

    # Run the program with the payload
    subprocess.run([bin_path, "--validate", payload, "invalidtoken"], capture_output=True)

    # Check if the injection succeeded
    assert os.path.isfile(pwned_path), "The payload did not successfully trigger the command injection to create the pwned file."