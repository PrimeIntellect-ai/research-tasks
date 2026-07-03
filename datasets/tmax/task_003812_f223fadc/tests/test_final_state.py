# test_final_state.py

import os
import stat
import hashlib
import urllib.request
import urllib.error
import ssl
import pytest

def test_rust_code_fixed_cwe295():
    main_rs = "/home/user/traffic-auditor/src/main.rs"
    assert os.path.isfile(main_rs), f"Missing main.rs at {main_rs}"

    with open(main_rs, "r", encoding="utf-8") as f:
        content = f.read()

    assert "danger_accept_invalid_certs(true)" not in content, \
        "The Rust code still contains 'danger_accept_invalid_certs(true)', meaning CWE-295 is not fixed."

def test_cookie_hash_file_exists_and_permissions():
    output_file = "/home/user/cookie_hash.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    # Check permissions (CWE-732)
    file_stat = os.stat(output_file)
    mode = file_stat.st_mode

    # We want exactly 0600 (rw-------)
    assert stat.S_IMODE(mode) == 0o600, \
        f"File permissions for {output_file} are not 0600. Current mode: {oct(stat.S_IMODE(mode))}"

def test_cookie_hash_content():
    # We should derive the expected hash by querying the local server, 
    # but since the server might be down or we just want to ensure it matches the known token:
    # The server always returns 'session_token=Th1sIsA_S3cr3t_T0k3n_8492; Secure; HttpOnly'

    # Let's try to fetch it from the server to be strictly principled, 
    # if the server is available. Otherwise fallback to the known token.
    expected_token = "Th1sIsA_S3cr3t_T0k3n_8492"

    try:
        ctx = ssl.create_default_context(cafile="/home/user/ca.crt")
        req = urllib.request.Request("https://127.0.0.1:8443/secure-endpoint")
        with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
            cookie_header = response.getheader('Set-Cookie')
            if cookie_header:
                # Extract session_token
                for part in cookie_header.split(';'):
                    part = part.strip()
                    if part.startswith('session_token='):
                        expected_token = part.split('=', 1)[1]
                        break
    except Exception:
        # Fallback to the known token if server fetch fails
        pass

    expected_hash = hashlib.sha256(expected_token.encode('utf-8')).hexdigest()

    output_file = "/home/user/cookie_hash.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    with open(output_file, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_hash, \
        f"The content of {output_file} does not match the expected SHA-256 hash of the cookie."