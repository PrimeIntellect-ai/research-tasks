# test_final_state.py

import os
import hashlib

def test_rotation_log_exists():
    path = "/home/user/rotation.log"
    assert os.path.isfile(path), f"Expected output file {path} is missing. Did the Rust program run and create it?"

def test_rotation_log_contents():
    path = "/home/user/rotation.log"
    assert os.path.isfile(path), f"Cannot check contents, {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Derived expected values based on task description
    expected_compromised_pass = "supersecret99"
    expected_attacker_ip = "192.168.133.7"
    new_password = "SecureRotation2024!"
    expected_new_pass_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

    expected_line1 = f"COMPROMISED_PASS: {expected_compromised_pass}"
    expected_line2 = f"ATTACKER_IP: {expected_attacker_ip}"
    expected_line3 = f"NEW_PASS_HASH: {expected_new_pass_hash}"

    assert expected_line1 in content, f"Log file does not contain the correct compromised password line. Expected: '{expected_line1}'"
    assert expected_line2 in content, f"Log file does not contain the correct attacker IP line. Expected: '{expected_line2}'"
    assert expected_line3 in content, f"Log file does not contain the correct new password hash line. Expected: '{expected_line3}'"

def test_rust_project_exists():
    cargo_toml_path = "/home/user/rotator/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Rust project not found at /home/user/rotator. {cargo_toml_path} is missing."