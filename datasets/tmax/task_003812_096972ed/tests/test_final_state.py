# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import json
import pytest

def test_rust_verifier_binary_exists():
    binary_path = "/home/user/app/verifier/target/release/verifier"
    assert os.path.isfile(binary_path), f"Rust verifier binary not found at {binary_path}. Did you compile with --release?"
    assert os.access(binary_path, os.X_OK), f"Rust verifier binary at {binary_path} is not executable."

def test_adversarial_corpus():
    binary_path = "/home/user/app/verifier/target/release/verifier"
    clean_dir = "/home/user/corpora/clean/"
    evil_dir = "/home/user/corpora/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed_clean = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(f))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_gateway_integration():
    import urllib.request

    # We will pick 5 clean files and 5 evil files
    clean_dir = "/home/user/corpora/clean/"
    evil_dir = "/home/user/corpora/evil/"

    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir)])[:5]
    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir)])[:5]

    # Send clean payloads
    for f in clean_files:
        with open(f, 'rb') as file:
            data = file.read()
        req = urllib.request.Request("http://127.0.0.1:8080/submit", data=data, method="POST")
        req.add_header('Content-Type', 'text/plain')
        try:
            response = urllib.request.urlopen(req, timeout=5)
            assert response.status == 200, f"Expected HTTP 200 for clean file {f}, got {response.status}"
        except urllib.error.HTTPError as e:
            pytest.fail(f"Expected HTTP 200 for clean file {f}, but got HTTP {e.code}")
        except Exception as e:
            pytest.fail(f"Failed to connect to gateway for clean file {f}: {e}")

    # Send evil payloads
    for f in evil_files:
        with open(f, 'rb') as file:
            data = file.read()
        req = urllib.request.Request("http://127.0.0.1:8080/submit", data=data, method="POST")
        req.add_header('Content-Type', 'text/plain')
        try:
            response = urllib.request.urlopen(req, timeout=5)
            pytest.fail(f"Expected HTTP 400 for evil file {f}, but got HTTP 200")
        except urllib.error.HTTPError as e:
            assert e.code == 400, f"Expected HTTP 400 for evil file {f}, got {e.code}"
        except Exception as e:
            pytest.fail(f"Failed to connect to gateway for evil file {f}: {e}")

def test_redis_integration():
    # Check that Redis contains exactly the 5 clean payloads we just sent
    try:
        # Assuming redis-cli is available
        result = subprocess.run(["redis-cli", "LLEN", "valid_builds"], capture_output=True, text=True, check=True)
        count = int(result.stdout.strip())
        assert count >= 5, f"Expected at least 5 items in valid_builds Redis list, got {count}"
    except Exception as e:
        pytest.fail(f"Failed to check Redis: {e}")