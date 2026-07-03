# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest
import requests

NEW_MASTER_KEY = "f4a8b2c9d3e7f1a5b6c0d4e8f2a9b3c7"
GATEWAY_URL = "http://127.0.0.1:8080/api/v1/data"
LOG_FILE = "/app/logs/backend.log"

def decrypt_aes_gcm(hex_ct: str, key: str) -> str:
    go_code = f"""package main
import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"fmt"
	"os"
)
func main() {{
	key := []byte("{key}")
	ct, err := hex.DecodeString(os.Args[1])
	if err != nil {{
		fmt.Print("hex_error")
		return
	}}
	block, err := aes.NewCipher(key)
	if err != nil {{
		fmt.Print("cipher_error")
		return
	}}
	aesgcm, err := cipher.NewGCM(block)
	if err != nil {{
		fmt.Print("gcm_error")
		return
	}}
	nonceSize := aesgcm.NonceSize()
	if len(ct) < nonceSize {{
		fmt.Print("length_error")
		return
	}}
	nonce, ciphertext := ct[:nonceSize], ct[nonceSize:]
	plaintext, err := aesgcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {{
		fmt.Print("decrypt_error")
		return
	}}
	fmt.Print(string(plaintext))
}}"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
        f.write(go_code)
        f_name = f.name

    try:
        res = subprocess.run(['go', 'run', f_name, hex_ct], capture_output=True, text=True)
        return res.stdout
    finally:
        os.remove(f_name)

def test_gateway_and_backend_integration():
    payload = {
        "user_token": "super_secret_xyz_123",
        "data": "secret_message"
    }

    try:
        response = requests.post(GATEWAY_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to gateway at {GATEWAY_URL}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    # Check CSP Header
    csp_header = response.headers.get("Content-Security-Policy", "")
    expected_csp = "default-src 'none'; frame-ancestors 'none';"
    assert expected_csp in csp_header, f"Missing or incorrect CSP header. Got: {csp_header}"

    # Check Response Body
    try:
        resp_json = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Gateway response is not valid JSON: {response.text}")

    assert "encrypted_data" in resp_json, f"Response JSON missing 'encrypted_data' field: {resp_json}"

    encrypted_hex = resp_json["encrypted_data"]

    # Decrypt and verify
    decrypted_text = decrypt_aes_gcm(encrypted_hex, NEW_MASTER_KEY)

    if decrypted_text in ["hex_error", "cipher_error", "gcm_error", "length_error", "decrypt_error"]:
        pytest.fail(f"Failed to decrypt the payload. Go decryption script returned: {decrypted_text}")

    assert decrypted_text == "secret_message", f"Decrypted text did not match expected 'secret_message'. Got: {decrypted_text}"

def test_logging_redaction():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."

    with open(LOG_FILE, "r") as f:
        log_contents = f.read()

    assert "super_secret_xyz_123" not in log_contents, "Sensitive data (user_token) was found in the logs!"
    assert "[REDACTED]" in log_contents, "The string '[REDACTED]' was not found in the logs."