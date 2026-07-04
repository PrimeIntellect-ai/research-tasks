# test_final_state.py

import os
import stat
import subprocess
import re

def run_test(payload, expected_status, expected_file=None):
    env = os.environ.copy()
    proc = subprocess.run(
        ["/app/upload_processor.sh"],
        input=payload.encode('utf-8'),
        capture_output=True,
        env=env
    )
    output = proc.stdout.decode('utf-8').strip()

    if expected_status not in output:
        return 0.0

    if expected_file:
        if not os.path.exists(expected_file):
            return 0.0
        mode = os.stat(expected_file).st_mode
        if stat.S_IMODE(mode) != 0o600:
            return 0.0

    return 1.0

def test_auth_config_rotated_and_secured():
    path = "/app/auth_config.env"
    assert os.path.exists(path), f"File {path} is missing."

    mode = os.stat(path).st_mode
    perms = stat.S_IMODE(mode)
    assert perms == 0o600, f"Permissions for {path} are {oct(perms)}, expected 0o600."

    with open(path, 'r') as f:
        content = f.read()

    token = None
    for line in content.splitlines():
        if line.startswith("ADMIN_TOKEN="):
            token = line.split("=", 1)[1].strip()
            break

    assert token is not None, f"ADMIN_TOKEN not found in {path}"
    assert token != "dex972", "ADMIN_TOKEN was not rotated from the leaked value 'dex972'."
    assert len(token) >= 32, f"ADMIN_TOKEN is too short (length {len(token)}), expected at least 32 characters."
    assert re.match(r'^[0-9a-fA-F]+$', token), "ADMIN_TOKEN is not a valid hex string."

def test_upload_processor_metric():
    path = "/app/auth_config.env"
    with open(path, 'r') as f:
        content = f.read()

    token = ""
    for line in content.splitlines():
        if line.startswith("ADMIN_TOKEN="):
            token = line.split("=", 1)[1].strip()
            break

    tests = [
        # 1. Valid request
        (f"Authorization: Bearer {token}\r\nX-Upload-Filename: test.wav\r\n\r\nBODY", "HTTP/1.1 200 OK", "/app/safe_uploads/test.wav"),
        # 2. Missing Auth
        ("X-Upload-Filename: test2.wav\r\n\r\nBODY", "HTTP/1.1 401 Unauthorized", None),
        # 3. Invalid Auth
        ("Authorization: Bearer BADTOKEN\r\nX-Upload-Filename: test3.wav\r\n\r\nBODY", "HTTP/1.1 401 Unauthorized", None),
        # 4. Path traversal attempt
        (f"Authorization: Bearer {token}\r\nX-Upload-Filename: ../../../etc/hack.wav\r\n\r\nBODY", "HTTP/1.1 200 OK", "/app/safe_uploads/hack.wav"),
        # 5. Bad extension
        (f"Authorization: Bearer {token}\r\nX-Upload-Filename: test.txt\r\n\r\nBODY", "HTTP/1.1 403 Forbidden", None),
    ]

    score = 0.0
    for payload, exp_status, exp_file in tests:
        if exp_file and os.path.exists(exp_file):
            os.remove(exp_file)
        score += run_test(payload, exp_status, exp_file)

    accuracy = score / len(tests)
    assert accuracy >= 1.0, f"Detection Accuracy metric failed. Got {accuracy:.2f}, expected 1.00."