# test_final_state.py

import os
import subprocess
import glob
import time
import pytest

def test_keys_and_certs_exist():
    expected_files = [
        "/home/user/old_pub.pem",
        "/home/user/new_key.pem",
        "/home/user/new_cert.pem",
        "/home/user/new_pub.pem",
        "/home/user/jwt_filter.py"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected file missing: {f}"

def generate_clean_tokens():
    # We must generate clean tokens dynamically using the agent's new key.
    # We will use the fixed PyJWT library to generate them.
    import sys
    sys.path.insert(0, "/app/vendor/PyJWT-1.7.1")
    import jwt

    with open("/home/user/new_key.pem", "rb") as f:
        private_key = f.read()

    clean_dir = "/app/corpora/clean"
    os.makedirs(clean_dir, exist_ok=True)

    # Generate a few clean tokens
    payloads = [
        {"sub": "user1", "role": "admin", "iat": int(time.time())},
        {"sub": "user2", "role": "user", "iat": int(time.time())}
    ]

    for i, payload in enumerate(payloads):
        token = jwt.encode(payload, private_key, algorithm="RS256")
        token_path = os.path.join(clean_dir, f"clean_{i}.jwt")
        with open(token_path, "wb") as f:
            f.write(token)

def test_jwt_filter_adversarial_corpus():
    # First generate the clean tokens
    generate_clean_tokens()

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"
    script_path = "/home/user/jwt_filter.py"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        result = subprocess.run(["python3", script_path, evil_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "REJECT":
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run(["python3", script_path, clean_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ACCEPT":
            clean_modified.append(os.path.basename(clean_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))