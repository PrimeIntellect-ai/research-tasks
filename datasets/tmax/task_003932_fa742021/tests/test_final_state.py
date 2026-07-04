# test_final_state.py
import os
import stat

def test_id_rsa_exists_and_permissions():
    path = "/home/user/.ssh/id_rsa"
    assert os.path.isfile(path), f"Private key file {path} does not exist. The key was not successfully extracted or saved to the correct location."

    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Private key {path} has incorrect permissions: {oct(perms)}. Expected 0o600 (standard SSH hardening)."

def test_id_rsa_pub_matches_truth():
    pub_path = "/home/user/.ssh/id_rsa.pub"
    truth_pub_path = "/tmp/temp_key.pub"

    assert os.path.isfile(pub_path), f"Public key file {pub_path} does not exist. You need to generate the public key from the extracted private key."
    assert os.path.isfile(truth_pub_path), f"Setup truth public key {truth_pub_path} is missing from the environment."

    with open(pub_path, 'r') as f:
        pub_parts = f.read().strip().split()

    with open(truth_pub_path, 'r') as f:
        truth_parts = f.read().strip().split()

    assert len(pub_parts) >= 2, f"Public key in {pub_path} is malformed or empty."
    assert len(truth_parts) >= 2, f"Truth public key in {truth_pub_path} is malformed."

    # Compare key type (e.g., ssh-rsa) and the base64 key blob
    assert pub_parts[0] == truth_parts[0], f"Public key type mismatch. Expected {truth_parts[0]}, got {pub_parts[0]}."
    assert pub_parts[1] == truth_parts[1], "Public key blob does not match the expected truth. The extracted private key might be incorrect."