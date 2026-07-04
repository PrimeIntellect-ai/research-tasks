# test_final_state.py

import os
import base64
import subprocess
import urllib.parse
import pytest

OLD_KEY = "0LDS3cR3T_123456"
NEW_KEY = "N3wS3cur3K3y9988"

def compute_signature(key: str, data: str) -> str:
    hash_val = 0
    input_str = key + data
    for c in input_str:
        hash_val = (hash_val * 31) + ord(c)
        hash_val &= 0xFFFFFFFF  # 32-bit unsigned integer
    return f"{hash_val:08x}"

def test_phase1_old_key():
    path = "/home/user/old_key.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == OLD_KEY, f"The extracted old key in {path} is incorrect."

def test_phase1_exploit_qs():
    path = "/home/user/exploit_qs.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        qs = f.read().strip()

    parsed = urllib.parse.parse_qs(qs, keep_blank_values=True)
    assert "payload" in parsed, "Exploit query string missing 'payload' parameter."
    assert "signature" in parsed, "Exploit query string missing 'signature' parameter."

    payload = parsed["payload"][0]
    signature = parsed["signature"][0]

    try:
        decoded_url = base64.b64decode(payload).decode('utf-8')
    except Exception:
        pytest.fail("Payload is not valid base64.")

    assert decoded_url == "http://attacker.com/steal", f"Decoded payload URL is '{decoded_url}', expected 'http://attacker.com/steal'."

    expected_sig = compute_signature(OLD_KEY, payload)
    assert signature == expected_sig, f"Signature in exploit query string is incorrect. Expected {expected_sig}, got {signature}."

def test_phase2_patched_cpp_exists():
    path = "/home/user/auth_server/login_handler_patched.cpp"
    assert os.path.isfile(path), f"Patched source file {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "extern const char* SECRET_KEY;" not in content, "The extern declaration for SECRET_KEY was not removed."
    assert NEW_KEY in content, "The new secret key is not hardcoded in the patched source file."

def test_phase2_patched_cgi_exists():
    path = "/home/user/auth_server/login_handler_patched.cgi"
    assert os.path.isfile(path), f"Compiled patched CGI {path} is missing."
    assert os.access(path, os.X_OK), f"Compiled patched CGI {path} is not executable."

def run_cgi(payload_str: str) -> str:
    payload_b64 = base64.b64encode(payload_str.encode()).decode('utf-8')
    # Remove padding as the custom base64 decoder in C++ might be strict or simple
    payload_b64 = payload_b64.rstrip('=')

    signature = compute_signature(NEW_KEY, payload_b64)
    qs = f"payload={payload_b64}&signature={signature}"

    env = os.environ.copy()
    env["QUERY_STRING"] = qs

    try:
        result = subprocess.run(
            ["/home/user/auth_server/login_handler_patched.cgi"],
            env=env,
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout
    except Exception as e:
        pytest.fail(f"Failed to execute the patched CGI: {e}")

def test_phase2_patched_cgi_valid_redirect():
    target = "/dashboard"
    stdout = run_cgi(target)
    assert "Location: /dashboard" in stdout, "Valid relative redirect failed to output the correct Location header."

def test_phase2_patched_cgi_malicious_redirect_absolute():
    target = "http://attacker.com/steal"
    stdout = run_cgi(target)
    assert "Location: /home" in stdout, "Absolute URL redirect was not defaulted to /home."

def test_phase2_patched_cgi_malicious_redirect_protocol_relative():
    target = "//attacker.com/steal"
    stdout = run_cgi(target)
    assert "Location: /home" in stdout, "Protocol-relative URL redirect (//...) was not defaulted to /home."

def test_phase2_patched_cgi_malicious_redirect_no_slash():
    target = "dashboard"
    stdout = run_cgi(target)
    assert "Location: /home" in stdout, "Relative URL not starting with a slash was not defaulted to /home."