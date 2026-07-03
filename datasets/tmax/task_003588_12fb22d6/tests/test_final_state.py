# test_final_state.py

import os
import stat
import subprocess
import tempfile
import pytest

def test_phase1_world_readable():
    output_file = "/home/user/world_readable.txt"
    assert os.path.exists(output_file), f"Phase 1 output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["file2.sql", "file4.log"]
    assert lines == expected, f"Expected {output_file} to contain {expected}, but got {lines}."

def test_phase2_fixed_keys():
    output_file = "/home/user/fixed_keys.txt"
    assert os.path.exists(output_file), f"Phase 2 output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["id_ecdsa", "id_rsa_2"]
    assert lines == expected, f"Expected {output_file} to contain {expected}, but got {lines}."

    # Verify that the keys actually have 600 permissions
    ssh_keys_dir = "/home/user/ssh_keys"
    for key_file in ["id_rsa_1", "id_rsa_2", "id_ecdsa"]:
        full_path = os.path.join(ssh_keys_dir, key_file)
        assert os.path.exists(full_path), f"SSH key {full_path} is missing."

        mode = os.stat(full_path).st_mode
        actual_perm = stat.S_IMODE(mode)
        assert actual_perm == 0o600, f"File {full_path} has incorrect permissions. Expected 0o600, got {oct(actual_perm)}."

def test_phase3_encryption_and_redaction():
    enc_file = "/home/user/secure_audit.enc"
    key_file = "/home/user/encryption_key.bin"

    assert os.path.exists(enc_file), f"Encrypted audit file {enc_file} is missing."
    assert os.path.exists(key_file), f"Encryption key file {key_file} is missing."

    # Since we cannot use third-party libraries (like cryptography) and the standard library
    # does not have AES-GCM, we use a small Go program to verify the decryption and redaction,
    # just as the verification script does. Go is guaranteed to be present as per the task.
    go_verifier = """
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"fmt"
	"io/ioutil"
	"os"
)

func main() {
	key, err := ioutil.ReadFile("/home/user/encryption_key.bin")
	if err != nil {
		fmt.Println("Failed to read key")
		os.Exit(1)
	}
	enc, err := ioutil.ReadFile("/home/user/secure_audit.enc")
	if err != nil {
		fmt.Println("Failed to read encrypted file")
		os.Exit(1)
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		fmt.Println("Failed to create cipher")
		os.Exit(1)
	}
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		fmt.Println("Failed to create GCM")
		os.Exit(1)
	}

	nonceSize := gcm.NonceSize()
	if len(enc) < nonceSize {
		fmt.Println("Encrypted file too short")
		os.Exit(1)
	}
	nonce, ciphertext := enc[:nonceSize], enc[nonceSize:]

	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		fmt.Println("Decryption failed (authentication or format error)")
		os.Exit(1)
	}

	expected := `System boot initiated.
User login Password: [REDACTED]
Connecting to remote server...
Error: auth failed.
Generating diagnostic dump.
Included keys:
[PRIVATE KEY REDACTED]
Diagnostic complete.
Admin authentication Password: [REDACTED]
End of log.
`
	if string(plaintext) != expected {
		fmt.Println("Redaction mismatch. Got:\\n" + string(plaintext))
		os.Exit(2)
	}
}
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=False) as f:
        f.write(go_verifier)
        temp_go_file = f.name

    try:
        result = subprocess.run(["go", "run", temp_go_file], capture_output=True, text=True)
        if result.returncode == 1:
            pytest.fail(f"Decryption failed: {result.stdout.strip()}")
        elif result.returncode == 2:
            pytest.fail(f"Redaction verification failed: {result.stdout.strip()}")
        elif result.returncode != 0:
            pytest.fail(f"Go verification script failed unexpectedly: {result.stderr.strip()}")
    finally:
        os.remove(temp_go_file)