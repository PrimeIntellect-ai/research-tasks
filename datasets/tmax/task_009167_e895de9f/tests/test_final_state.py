# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_ssh_keys_quarantined_and_fingerprints():
    # Check that insecure keys are in quarantine
    quarantine_dir = "/home/user/quarantine_keys"
    assert os.path.isdir(quarantine_dir), f"Quarantine directory {quarantine_dir} is missing."

    # Expected secure keys
    secure_keys = ["id_rsa_4096", "id_ecdsa_256"]
    secure_keys_file = "/home/user/secure_keys.txt"

    assert os.path.isfile(secure_keys_file), f"{secure_keys_file} is missing."

    with open(secure_keys_file, "r") as f:
        content = f.read().strip()

    for key in secure_keys:
        pub_key_path = f"/home/user/ssh_audit/{key}.pub"
        if not os.path.exists(pub_key_path):
            # Fallback if they moved the pub keys too
            pub_key_path = f"/home/user/ssh_audit/{key}"

        # Compute fingerprint
        try:
            result = subprocess.run(
                ["ssh-keygen", "-l", "-f", pub_key_path],
                capture_output=True, text=True, check=True
            )
            fingerprint = result.stdout.strip()
            # The exact output of ssh-keygen -l might vary slightly, so check if the hash part is in the file
            hash_part = fingerprint.split()[1]
            assert hash_part in content, f"Fingerprint for {key} ({hash_part}) not found in {secure_keys_file}."
        except subprocess.CalledProcessError:
            pytest.fail(f"Could not compute fingerprint for {pub_key_path}")

def test_artifacts_corrupted_files():
    corrupted_file = "/home/user/corrupted_files.txt"
    assert os.path.isfile(corrupted_file), f"{corrupted_file} is missing."

    with open(corrupted_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = {"lib_v1.bin", "data_v1.bin"}
    actual = set(lines)

    assert expected.issubset(actual), f"Expected corrupted files {expected} not fully found in {corrupted_file}. Found: {actual}"
    assert len(actual) == 2, f"Expected exactly 2 corrupted files, found {len(actual)}: {actual}"

def test_auth_script_and_user():
    valid_user_file = "/home/user/valid_user.txt"
    assert os.path.isfile(valid_user_file), f"{valid_user_file} is missing."

    with open(valid_user_file, "r") as f:
        user = f.read().strip()

    assert user == "charlie", f"Expected valid user 'charlie', found '{user}'."

    secret_key_path = "/home/user/auth/secret.key"
    assert os.path.isfile(secret_key_path), f"{secret_key_path} is missing."

    st = os.stat(secret_key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Expected permissions 0600 on {secret_key_path}, got {oct(perms)}"

    login_check_path = "/home/user/auth/login_check.py"
    assert os.path.isfile(login_check_path), f"{login_check_path} is missing."

    with open(login_check_path, "r") as f:
        script_content = f.read()

    assert "hmac.compare_digest" in script_content, f"hmac.compare_digest not found in {login_check_path}"
    assert "hashlib.sha256" in script_content, f"hashlib.sha256 not found in {login_check_path}"