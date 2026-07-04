# test_final_state.py
import os
import subprocess
import pytest
import urllib.request
import urllib.error
import ssl

def test_filter_script_exists():
    assert os.path.isfile('/home/user/filter.py'), "/home/user/filter.py is missing"

def test_corpus_validation():
    clean_dir = '/app/corpus/clean/'
    evil_dir = '/app/corpus/evil/'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for f in clean_files:
        result = subprocess.run(['python3', '/home/user/filter.py', f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run(['python3', '/home/user/filter.py', f], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_nginx_mtls_and_flask_integration():
    # Test 1: No client cert -> should fail
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        urllib.request.urlopen("https://127.0.0.1:8443/login?token=dummy", context=ctx, timeout=5)
        pytest.fail("Nginx accepted connection without client certificate")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 for missing client cert, got {e.code}"
    except urllib.error.URLError:
        pass # Connection reset or similar is also acceptable for missing cert

    # Test 2: Valid client cert, clean token -> should redirect (302)
    # Generate a valid token for https://internal.corp.local/dashboard
    url = "https://internal.corp.local/dashboard"
    key = "N3tw0rkS3cur1tyK3y"
    encrypted = bytes(ord(url[i]) ^ ord(key[i % len(key)]) for i in range(len(url))).hex()

    curl_cmd_valid = [
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "--key", "/app/certs/client.key",
        "--cert", "/app/certs/client.crt",
        "--cacert", "/app/certs/ca.crt",
        f"https://127.0.0.1:8443/login?token={encrypted}"
    ]

    result = subprocess.run(curl_cmd_valid, capture_output=True, text=True)
    assert result.stdout.strip() in ["302", "301"], f"Expected redirect (302) for valid token, got HTTP {result.stdout.strip()}"

    # Test 3: Valid client cert, evil token -> should be 403 Forbidden
    evil_url = "http://evil.attacker.com/phish"
    encrypted_evil = bytes(ord(evil_url[i]) ^ ord(key[i % len(key)]) for i in range(len(evil_url))).hex()

    curl_cmd_evil = [
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "--key", "/app/certs/client.key",
        "--cert", "/app/certs/client.crt",
        "--cacert", "/app/certs/ca.crt",
        f"https://127.0.0.1:8443/login?token={encrypted_evil}"
    ]

    result_evil = subprocess.run(curl_cmd_evil, capture_output=True, text=True)
    assert result_evil.stdout.strip() == "403", f"Expected 403 Forbidden for evil token, got HTTP {result_evil.stdout.strip()}"