# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest

SUMMARY_PATH = "/home/user/rotation_summary.json"
KEYS_DIR = "/home/user/keys"
SECRET_PATH = "/home/user/master.secret"

def base64url_decode(input_str):
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def base64url_encode(input_bytes):
    return base64.urlsafe_b64encode(input_bytes).decode('utf-8').rstrip('=')

def test_summary_exists_and_format():
    assert os.path.isfile(SUMMARY_PATH), f"Summary file missing at {SUMMARY_PATH}"

    with open(SUMMARY_PATH, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Summary file is not valid JSON")

    expected_users = {"bob", "david"}
    actual_users = set(summary.keys())
    assert actual_users == expected_users, f"Expected compromised users {expected_users}, found {actual_users}"

    for user in expected_users:
        assert "pub_key" in summary[user], f"Missing pub_key for {user}"
        assert "token" in summary[user], f"Missing token for {user}"

def test_ssh_keys_created_and_match():
    with open(SUMMARY_PATH, "r") as f:
        summary = json.load(f)

    for user in ["bob", "david"]:
        pub_key_path = os.path.join(KEYS_DIR, f"{user}_id_ed25519.pub")
        priv_key_path = os.path.join(KEYS_DIR, f"{user}_id_ed25519")

        assert os.path.isfile(pub_key_path), f"Public key missing at {pub_key_path}"
        assert os.path.isfile(priv_key_path), f"Private key missing at {priv_key_path}"

        with open(pub_key_path, "r") as f:
            actual_pub_key = f.read().strip()

        assert summary[user]["pub_key"].strip() == actual_pub_key, f"pub_key in summary does not match file for {user}"

def test_jwt_tokens_valid():
    assert os.path.isfile(SECRET_PATH), "Master secret file missing"
    with open(SECRET_PATH, "r") as f:
        secret = f.read().strip().encode('utf-8')

    with open(SUMMARY_PATH, "r") as f:
        summary = json.load(f)

    for user in ["bob", "david"]:
        token = summary[user]["token"]
        parts = token.split(".")
        assert len(parts) == 3, f"Token for {user} is not in 3 parts"

        header_b64, payload_b64, sig_b64 = parts

        header = json.loads(base64url_decode(header_b64).decode('utf-8'))
        payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))

        assert header.get("alg") == "HS256"
        assert header.get("typ") == "JWT"

        assert payload.get("user") == user
        assert payload.get("action") == "key_rotation"

        msg = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = base64url_encode(hmac.new(secret, msg, hashlib.sha256).digest())

        assert sig_b64 == expected_sig, f"Invalid token signature for {user}"