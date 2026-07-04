# test_final_state.py

import os
import subprocess
import pytest

def test_chain_pem_extracted():
    user_chain_path = "/home/user/chain.pem"
    dropper_path = "/home/user/evidence/dropper.elf"
    truth_chain_path = "/tmp/truth_chain.pem"

    assert os.path.isfile(user_chain_path), f"{user_chain_path} is missing"
    assert os.path.isfile(dropper_path), f"{dropper_path} is missing"

    # Extract the .evil_cert section to a temporary file to compare
    try:
        subprocess.run(
            ['objcopy', '-O', 'binary', '--only-section=.evil_cert', dropper_path, truth_chain_path],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract .evil_cert section for verification: {e}")

    assert os.path.isfile(truth_chain_path), "Failed to create truth extraction file"

    with open(user_chain_path, 'rb') as f:
        user_chain = f.read()

    with open(truth_chain_path, 'rb') as f:
        truth_chain = f.read()

    # Clean up the temporary file
    os.remove(truth_chain_path)

    assert user_chain == truth_chain, f"The contents of {user_chain_path} do not exactly match the .evil_cert section"

def test_root_ca_cn():
    cn_file_path = "/home/user/root_ca_cn.txt"
    assert os.path.isfile(cn_file_path), f"{cn_file_path} is missing"

    with open(cn_file_path, "r") as f:
        content = f.read().strip()

    expected_cn = "Rogue Root CA"
    assert content == expected_cn, f"Expected Root CA CN to be '{expected_cn}', but got '{content}'"

def test_crack_cpp_exists():
    cpp_file_path = "/home/user/crack.cpp"
    assert os.path.isfile(cpp_file_path), f"{cpp_file_path} is missing"

def test_decrypted_data():
    decrypted_file_path = "/home/user/decrypted_data.txt"
    assert os.path.isfile(decrypted_file_path), f"{decrypted_file_path} is missing"

    with open(decrypted_file_path, "r") as f:
        content = f.read().strip()

    expected_plaintext = "CONFIDENTIAL: The main server backdoor password is 'RogueAccess2024!'. Do not share."
    assert content == expected_plaintext, f"The decrypted data does not match the expected plaintext. Got: '{content}'"