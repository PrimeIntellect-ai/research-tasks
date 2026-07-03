# test_final_state.py

import os
import json
import subprocess
import base64

def _base64url_decode(data: str) -> bytes:
    """Helper to decode base64url encoded strings (adding padding if necessary)."""
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def _base64url_encode(data: bytes) -> str:
    """Helper to encode to base64url without padding."""
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def test_block_ips_script_exists_and_executable():
    """Validates that block_ips.sh exists and is executable."""
    script_path = "/home/user/block_ips.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_craft_jwt_script_exists_and_executable():
    """Validates that craft_jwt.sh exists and is executable."""
    script_path = "/home/user/craft_jwt.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_block_ips_generates_correct_policy():
    """
    Executes block_ips.sh, derives the expected malicious IPs from the log file,
    and verifies that deny_policy.json exactly matches the derived expected state.
    """
    script_path = "/home/user/block_ips.sh"
    log_path = "/home/user/gateway.log"
    policy_path = "/home/user/deny_policy.json"

    # Remove policy file if it exists to ensure the script creates it
    if os.path.exists(policy_path):
        os.remove(policy_path)

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}"

    assert os.path.isfile(policy_path), f"Script did not generate the expected policy file at {policy_path}"

    # Derive expected IPs from the log
    expected_ips = set()
    with open(log_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get("status") == 200:
                    auth_header = entry.get("auth_header", "")
                    if auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]
                        parts = token.split(".")
                        if len(parts) >= 1:
                            header_b64 = parts[0]
                            header_json = json.loads(_base64url_decode(header_b64).decode('utf-8'))
                            if header_json.get("alg", "").lower() == "none":
                                expected_ips.add(entry.get("ip"))
            except Exception:
                continue

    expected_ips_sorted = sorted(list(expected_ips))

    # Read the generated policy
    with open(policy_path, 'r') as f:
        try:
            policy_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Generated file {policy_path} is not valid JSON."

    assert "blocked_ips" in policy_data, f"Generated policy missing 'blocked_ips' key. Found keys: {list(policy_data.keys())}"

    actual_ips = policy_data["blocked_ips"]
    assert isinstance(actual_ips, list), "'blocked_ips' must be a JSON array."

    assert actual_ips == expected_ips_sorted, f"Blocked IPs do not match expected. Expected: {expected_ips_sorted}, Got: {actual_ips}"

def test_craft_jwt_output():
    """
    Executes craft_jwt.sh with a test username and verifies the generated JWT
    matches the exact expected Base64Url encoded structure.
    """
    script_path = "/home/user/craft_jwt.sh"
    test_user = "test_validator_user"

    result = subprocess.run([script_path, test_user], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}"

    output_token = result.stdout.strip()

    # Derive expected token
    header = {"alg": "none", "typ": "JWT"}
    payload = {"user": test_user, "role": "admin"}

    header_enc = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_enc = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))

    expected_token = f"{header_enc}.{payload_enc}."

    assert output_token == expected_token, f"Crafted JWT is incorrect.\nExpected: {expected_token}\nGot:      {output_token}"