# test_final_state.py
import json
import os
import subprocess
import base64

def test_result_json_exists_and_valid():
    assert os.path.isfile("/home/user/result.json"), "/home/user/result.json does not exist"
    with open("/home/user/result.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/result.json is not valid JSON"

    assert "crafted_jwt" in data, "Missing crafted_jwt in result.json"
    assert "rotation_id" in data, "Missing rotation_id in result.json"

def test_crafted_jwt():
    with open("/home/user/result.json", "r") as f:
        data = json.load(f)
    jwt = data["crafted_jwt"]
    parts = jwt.split(".")
    assert len(parts) == 3, "JWT must have exactly 3 parts separated by dots"

    def decode_b64(s):
        s = s.replace("-", "+").replace("_", "/")
        s += "=" * ((4 - len(s) % 4) % 4)
        return base64.b64decode(s)

    try:
        header = json.loads(decode_b64(parts[0]))
        payload = json.loads(decode_b64(parts[1]))
    except Exception as e:
        assert False, f"Failed to decode JWT header or payload: {e}"

    assert header.get("alg") == "none", "JWT header 'alg' must be 'none'"
    assert payload.get("role") == "admin", "JWT payload 'role' must be 'admin'"

def test_rotation_id_matches_log():
    assert os.path.isfile("/home/user/app/audit.log"), "/home/user/app/audit.log does not exist"
    with open("/home/user/result.json", "r") as f:
        data = json.load(f)
    expected_id = data["rotation_id"]

    # Python stdlib does not have AES-GCM. 
    # Since Go is available in the environment, we use a small Go helper to decrypt the logs.
    go_script = """package main
import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"fmt"
	"os"
	"strings"
)
func main() {
	logKey := []byte("supersecret32bytekey123456789012")
	data, err := os.ReadFile("/home/user/app/audit.log")
	if err != nil { return }
	lines := strings.Split(strings.TrimSpace(string(data)), "\\n")
	for _, line := range lines {
		if line == "" { continue }
		decoded, err := base64.StdEncoding.DecodeString(line)
		if err != nil { continue }
		block, err := aes.NewCipher(logKey)
		if err != nil { continue }
		gcm, err := cipher.NewGCM(block)
		if err != nil { continue }
		nonceSize := gcm.NonceSize()
		if len(decoded) < nonceSize { continue }
		nonce, ciphertext := decoded[:nonceSize], decoded[nonceSize:]
		plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
		if err == nil {
			fmt.Println(string(plaintext))
		}
	}
}
"""
    helper_path = "/tmp/decrypt_test_helper.go"
    with open(helper_path, "w") as f:
        f.write(go_script)

    res = subprocess.run(["go", "run", helper_path], capture_output=True, text=True)
    assert res.returncode == 0, "Failed to run Go decryption helper"

    decrypted_logs = res.stdout
    assert expected_id in decrypted_logs, f"Rotation ID '{expected_id}' from result.json was not found in the decrypted audit logs."