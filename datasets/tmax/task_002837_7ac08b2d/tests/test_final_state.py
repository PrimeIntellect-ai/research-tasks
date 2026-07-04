# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import tempfile
import json
import base64

def test_classifier_script():
    classifier_path = "/home/user/classifier.py"
    assert os.path.isfile(classifier_path), f"Classifier script missing at {classifier_path}"

    clean_file = "/home/user/corpus/clean/tokens.txt"
    evil_file = "/home/user/corpus/evil/tokens.txt"

    assert os.path.isfile(clean_file), f"Clean corpus missing: {clean_file}"
    assert os.path.isfile(evil_file), f"Evil corpus missing: {evil_file}"

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as clean_out:
        clean_out_path = clean_out.name
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as evil_out:
        evil_out_path = evil_out.name

    try:
        subprocess.run(["python3", classifier_path, clean_file, clean_out_path], check=True, capture_output=True)
        subprocess.run(["python3", classifier_path, evil_file, evil_out_path], check=True, capture_output=True)

        with open(clean_file, "r") as f:
            clean_lines = f.read().splitlines()
        with open(clean_out_path, "r") as f:
            clean_out_lines = f.read().splitlines()

        with open(evil_file, "r") as f:
            evil_lines = f.read().splitlines()
        with open(evil_out_path, "r") as f:
            evil_out_lines = f.read().splitlines()

        assert len(clean_lines) == len(clean_out_lines), f"Clean output length mismatch. Expected {len(clean_lines)}, got {len(clean_out_lines)}"
        assert len(evil_lines) == len(evil_out_lines), f"Evil output length mismatch. Expected {len(evil_lines)}, got {len(evil_out_lines)}"

        clean_modified = []
        for i, res in enumerate(clean_out_lines):
            if res.strip() != "CLEAN":
                clean_modified.append(f"Line {i+1}")

        evil_bypassed = []
        for i, res in enumerate(evil_out_lines):
            if res.strip() != "EVIL":
                evil_bypassed.append(f"Line {i+1}")

        error_msg = ""
        if evil_bypassed:
            error_msg += f"{len(evil_bypassed)} of {len(evil_lines)} evil bypassed: {', '.join(evil_bypassed[:5])}\n"
        if clean_modified:
            error_msg += f"{len(clean_modified)} of {len(clean_lines)} clean modified: {', '.join(clean_modified[:5])}\n"

        assert not error_msg, error_msg

    finally:
        if os.path.exists(clean_out_path):
            os.remove(clean_out_path)
        if os.path.exists(evil_out_path):
            os.remove(evil_out_path)

def test_nginx_auth_request():
    clean_file = "/home/user/corpus/clean/tokens.txt"
    evil_file = "/home/user/corpus/evil/tokens.txt"

    with open(clean_file, "r") as f:
        clean_token = f.readline().strip()
    with open(evil_file, "r") as f:
        evil_token = f.readline().strip()

    # Test clean token
    req_clean = urllib.request.Request("http://127.0.0.1:8000/api/data")
    req_clean.add_header("Cookie", f"auth_token={clean_token}")
    try:
        with urllib.request.urlopen(req_clean) as response:
            assert response.status == 200, f"Expected 200 OK for clean token, got {response.status}"
    except urllib.error.HTTPError as e:
        assert False, f"Expected 200 OK for clean token, got HTTPError: {e.code}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on port 8000: {e.reason}"

    # Test evil token
    req_evil = urllib.request.Request("http://127.0.0.1:8000/api/data")
    req_evil.add_header("Cookie", f"auth_token={evil_token}")
    try:
        with urllib.request.urlopen(req_evil) as response:
            assert False, f"Expected 401 Unauthorized for evil token, got {response.status}"
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401 Unauthorized for evil token, got {e.code}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on port 8000: {e.reason}"

    # Test missing token
    req_missing = urllib.request.Request("http://127.0.0.1:8000/api/data")
    try:
        with urllib.request.urlopen(req_missing) as response:
            assert False, f"Expected 401 Unauthorized for missing token, got {response.status}"
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401 Unauthorized for missing token, got {e.code}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on port 8000: {e.reason}"