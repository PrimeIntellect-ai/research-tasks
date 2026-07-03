# test_final_state.py

import os
import pytest

def test_decrypted_policy_exists_and_correct():
    decrypted_path = "/home/user/decrypted_policy.txt"
    assert os.path.exists(decrypted_path), f"File {decrypted_path} does not exist. Did you save the decrypted output?"
    assert os.path.isfile(decrypted_path), f"Path {decrypted_path} is not a file."

    with open(decrypted_path, "r") as f:
        content = f.read()

    expected_content = "POLICY=DENY_UNTRUSTED_REGISTRIES"
    assert content == expected_content, f"The decrypted policy content is incorrect. Expected exactly '{expected_content}', but got '{content}'"

def test_decoder_rs_exists():
    decoder_path = "/home/user/decoder.rs"
    assert os.path.exists(decoder_path), f"Rust program {decoder_path} does not exist. Did you write the solution in Rust?"
    assert os.path.isfile(decoder_path), f"Path {decoder_path} is not a file."