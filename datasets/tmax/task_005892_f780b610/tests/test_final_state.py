# test_final_state.py

import os
import subprocess
import hashlib

CREDENTIALS_DIR = '/home/user/credentials'
SERVICE_KEY = os.path.join(CREDENTIALS_DIR, 'service_key')
SERVICE_KEY_PUB = os.path.join(CREDENTIALS_DIR, 'service_key.pub')
ENCODER_C = os.path.join(CREDENTIALS_DIR, 'encoder.c')
ENCODER_BIN = os.path.join(CREDENTIALS_DIR, 'encoder')
OBFUSCATED_PAYLOAD = os.path.join(CREDENTIALS_DIR, 'obfuscated_payload.txt')
PAYLOAD_CHECKSUM = os.path.join(CREDENTIALS_DIR, 'payload_checksum.txt')

def test_credentials_dir_exists():
    assert os.path.isdir(CREDENTIALS_DIR), f"Directory {CREDENTIALS_DIR} does not exist."

def test_ssh_key_exists_and_valid():
    assert os.path.isfile(SERVICE_KEY), f"Private key {SERVICE_KEY} does not exist."
    assert os.path.isfile(SERVICE_KEY_PUB), f"Public key {SERVICE_KEY_PUB} does not exist."

    # Check if it's a valid ed25519 key
    result = subprocess.run(
        ['ssh-keygen', '-l', '-f', SERVICE_KEY],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"ssh-keygen validation failed for {SERVICE_KEY}:\n{result.stderr}"
    assert "ED25519" in result.stdout.upper(), f"The key {SERVICE_KEY} does not appear to be an ed25519 key."

def test_encoder_files_exist():
    assert os.path.isfile(ENCODER_C), f"Source file {ENCODER_C} does not exist."
    assert os.path.isfile(ENCODER_BIN), f"Executable {ENCODER_BIN} does not exist."
    assert os.access(ENCODER_BIN, os.X_OK), f"File {ENCODER_BIN} is not executable."

def test_obfuscated_payload():
    assert os.path.isfile(OBFUSCATED_PAYLOAD), f"Payload file {OBFUSCATED_PAYLOAD} does not exist."

    with open(SERVICE_KEY_PUB, 'rb') as f:
        pub_key = f.read()

    expected_obfuscated = ''.join([f"{b ^ 0x5C:02X}" for b in pub_key]).encode('utf-8')

    with open(OBFUSCATED_PAYLOAD, 'rb') as f:
        actual_obfuscated = f.read()

    assert expected_obfuscated == actual_obfuscated, "Obfuscated payload does not match expected XOR hex output."

def test_payload_checksum():
    assert os.path.isfile(PAYLOAD_CHECKSUM), f"Checksum file {PAYLOAD_CHECKSUM} does not exist."

    with open(OBFUSCATED_PAYLOAD, 'rb') as f:
        payload_data = f.read()

    expected_hash = hashlib.sha256(payload_data).hexdigest()

    with open(PAYLOAD_CHECKSUM, 'r') as f:
        actual_hash = f.read().strip()

    assert expected_hash == actual_hash, "Checksum does not match the sha256 of the obfuscated payload."