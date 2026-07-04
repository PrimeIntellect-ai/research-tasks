# test_final_state.py

import os
import sys
import hashlib
import subprocess
import tempfile
import re
import pytest

def test_stage1_vendored_package_fixed():
    api_jwt_path = "/app/vendored/pyjwt-2.8.0/jwt/api_jwt.py"
    assert os.path.isfile(api_jwt_path), f"Missing api_jwt.py at {api_jwt_path}"

    with open(api_jwt_path, "r") as f:
        content = f.read()

    assert 'raise DecodeError("Task perturbation")' not in content, "The deliberate perturbation was not removed from api_jwt.py"

def test_stage2_and_4_valid_users_and_checksum():
    # Insert vendored package to sys.path to use it for validation
    vendored_path = "/app/vendored/pyjwt-2.8.0"
    if vendored_path not in sys.path:
        sys.path.insert(0, vendored_path)

    try:
        import jwt
    except ImportError:
        pytest.fail("Failed to import jwt from the vendored package.")

    secret_path = "/home/user/jwt_secret.key"
    tokens_path = "/home/user/captured_tokens.txt"
    users_log_path = "/home/user/valid_users.log"
    checksum_path = "/home/user/audit_checksum.txt"

    assert os.path.isfile(secret_path), "Missing jwt_secret.key"
    assert os.path.isfile(tokens_path), "Missing captured_tokens.txt"
    assert os.path.isfile(users_log_path), "Missing valid_users.log"
    assert os.path.isfile(checksum_path), "Missing audit_checksum.txt"

    with open(secret_path, "r") as f:
        secret = f.read().strip()

    with open(tokens_path, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    expected_users = []
    for token in tokens:
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            if "user_id" in decoded:
                expected_users.append(str(decoded["user_id"]))
        except Exception:
            pass

    expected_users.sort()
    expected_log_content = "\n".join(expected_users) + ("\n" if expected_users else "")

    with open(users_log_path, "r") as f:
        actual_log_content = f.read()

    assert actual_log_content.strip() == expected_log_content.strip(), "valid_users.log does not contain the correct sorted user_ids."

    expected_checksum = hashlib.sha256(actual_log_content.encode('utf-8')).hexdigest()

    with open(checksum_path, "r") as f:
        actual_checksum = f.read().strip()

    assert actual_checksum == expected_checksum, "audit_checksum.txt does not match the SHA-256 checksum of valid_users.log"

def test_stage3_redactor_adversarial_corpus():
    redactor_script = "/home/user/redactor.py"
    assert os.path.isfile(redactor_script), f"Missing redactor script at {redactor_script}"

    evil_corpus = "/app/corpora/evil/"
    clean_corpus = "/app/corpora/clean/"

    assert os.path.isdir(evil_corpus), "Missing evil corpus directory"
    assert os.path.isdir(clean_corpus), "Missing clean corpus directory"

    evil_files = [f for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    clean_files = [f for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]

    evil_bypassed = []
    clean_modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test evil corpus
        for filename in evil_files:
            input_path = os.path.join(evil_corpus, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                [sys.executable, redactor_script, input_path, output_path],
                capture_output=True, text=True
            )

            if result.returncode != 0 or not os.path.isfile(output_path):
                evil_bypassed.append(filename)
                continue

            with open(input_path, "r") as f:
                input_data = f.read()
            with open(output_path, "r") as f:
                output_data = f.read()

            if input_data == output_data or "[REDACTED]" not in output_data:
                evil_bypassed.append(filename)

        # Test clean corpus
        for filename in clean_files:
            input_path = os.path.join(clean_corpus, filename)
            output_path = os.path.join(tmpdir, filename)

            result = subprocess.run(
                [sys.executable, redactor_script, input_path, output_path],
                capture_output=True, text=True
            )

            if result.returncode != 0 or not os.path.isfile(output_path):
                clean_modified.append(filename)
                continue

            with open(input_path, "r") as f:
                input_data = f.read()
            with open(output_path, "r") as f:
                output_data = f.read()

            if input_data != output_data:
                clean_modified.append(filename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))