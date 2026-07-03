# test_final_state.py

import os
import stat
import base64
import subprocess
import pytest

def test_secrets_directory_and_key():
    key_path = "/home/user/.secrets/new_aes.key"
    assert os.path.isfile(key_path), f"File {key_path} is missing."

    st = os.stat(key_path)
    assert stat.S_IMODE(st.st_mode) == 0o600, f"Permissions for {key_path} are not 0600."

    with open(key_path, "r") as f:
        content = f.read().strip()

    try:
        key_bytes = base64.b64decode(content)
        assert len(key_bytes) == 32, "Decoded AES key is not 32 bytes."
    except Exception as e:
        pytest.fail(f"Failed to base64 decode the AES key: {e}")

def test_ssh_key_permissions():
    ssh_key_path = "/home/user/.ssh/new_service_key"
    assert os.path.isfile(ssh_key_path), f"File {ssh_key_path} is missing."

    st = os.stat(ssh_key_path)
    assert stat.S_IMODE(st.st_mode) == 0o600, f"Permissions for {ssh_key_path} are not 0600."

def test_go_and_shell_scripts_exist():
    assert os.path.isfile("/home/user/rotate.go"), "/home/user/rotate.go is missing."
    assert os.path.isfile("/home/user/run.sh"), "/home/user/run.sh is missing."

def test_encrypted_ips_payload():
    enc_path = "/home/user/data/ips_secured.enc"
    assert os.path.isfile(enc_path), f"File {enc_path} is missing."

    # We use a small Go program to verify the AES-GCM decryption since Go is available 
    # and we cannot use third-party Python libraries like cryptography.
    verifier_go = """package main
import (
    "crypto/aes"
    "crypto/cipher"
    "encoding/base64"
    "encoding/hex"
    "fmt"
    "os"
    "strings"
)
func main() {
    keyB64, err := os.ReadFile("/home/user/.secrets/new_aes.key")
    if err != nil { os.Exit(1) }
    key, err := base64.StdEncoding.DecodeString(strings.TrimSpace(string(keyB64)))
    if err != nil { os.Exit(2) }

    encHex, err := os.ReadFile("/home/user/data/ips_secured.enc")
    if err != nil { os.Exit(3) }
    encBytes, err := hex.DecodeString(strings.TrimSpace(string(encHex)))
    if err != nil { os.Exit(4) }

    if len(encBytes) < 12 { os.Exit(5) }

    block, err := aes.NewCipher(key)
    if err != nil { os.Exit(6) }

    aesgcm, err := cipher.NewGCM(block)
    if err != nil { os.Exit(7) }

    nonce := encBytes[:12]
    ciphertext := encBytes[12:]

    plaintext, err := aesgcm.Open(nil, nonce, ciphertext, nil)
    if err != nil { os.Exit(8) }

    fmt.Print(string(plaintext))
}
"""
    verifier_path = "/tmp/verify_decryption.go"
    with open(verifier_path, "w") as f:
        f.write(verifier_go)

    result = subprocess.run(["go", "run", verifier_path], capture_output=True, text=True)

    if result.returncode != 0:
        pytest.fail(f"Failed to decrypt ips_secured.enc using the new AES key. Go exit code: {result.returncode}")

    plaintext = result.stdout.strip()

    expected_ips = {"192.168.1.50", "10.0.0.5", "203.0.113.42"}
    actual_ips = set(ip.strip() for ip in plaintext.split(","))

    assert actual_ips == expected_ips, f"Decrypted payload does not contain the correct IPs. Got: {plaintext}"