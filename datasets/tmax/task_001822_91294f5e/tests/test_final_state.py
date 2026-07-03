# test_final_state.py
import os
import stat
import urllib.request
import ssl
import time
import pytest

def test_makefile_fixed():
    makefile_path = "/app/legacy-tls-server-1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "python3 " in content, "The typo 'pyton3' in the Makefile was not fixed to 'python3'."
    assert "pyton3 " not in content, "The typo 'pyton3' is still present in the Makefile."

def test_credentials_exist_and_secure():
    passphrase_file = "/home/user/passphrase.key"
    cert_file = "/home/user/certs/server.crt"
    key_file = "/home/user/certs/server.key"

    assert os.path.isfile(passphrase_file), f"Passphrase file missing at {passphrase_file}"
    st = os.stat(passphrase_file)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Passphrase file permissions are {oct(permissions)}, expected 0o400."

    assert os.path.isfile(cert_file), f"Certificate missing at {cert_file}"
    assert os.path.isfile(key_file), f"Private key missing at {key_file}"

    with open(key_file, "r") as f:
        key_content = f.read()

    # Check if the key is encrypted (PEM format usually contains ENCRYPTED for encrypted keys)
    assert "ENCRYPTED" in key_content, "The private key does not appear to be encrypted."

def test_deployment_done_log():
    log_file = "/home/user/deployment_done.log"
    assert os.path.isfile(log_file), f"Deployment log missing at {log_file}"

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == "READY", f"Deployment log content is '{content}', expected 'READY'."

def test_isolation_score():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    attempts = [
        "/etc/passwd",
        "/home/user/secrets/flag.txt"
    ]
    blocked = 0

    # Wait briefly to ensure the server is up
    server_up = False
    for _ in range(10):
        try:
            urllib.request.urlopen("https://127.0.0.1:8443/", context=ctx, timeout=1)
            server_up = True
            break
        except Exception:
            time.sleep(0.5)

    assert server_up, "Server is not reachable on https://127.0.0.1:8443. Ensure secure_runner.sh starts the server."

    for f in attempts:
        try:
            req = urllib.request.urlopen(f"https://127.0.0.1:8443/read?file={f}", context=ctx, timeout=2)
            res = req.read()
            if b"Not Found" in res:
                blocked += 1
        except Exception:
            # Any exception (like connection reset due to bwrap restrictions) counts as blocked
            blocked += 1

    isolation_score = blocked / len(attempts)
    assert isolation_score >= 1.0, f"isolation_score is {isolation_score}, expected >= 1.0. Some LFI attempts succeeded."