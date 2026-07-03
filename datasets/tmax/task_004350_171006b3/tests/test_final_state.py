# test_final_state.py
import os
import json
import subprocess
import urllib.request

def test_flask_health():
    """Verify that the Flask app is up and returns status ok."""
    try:
        req = urllib.request.Request("http://localhost:5000/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            assert data.get("status") == "ok", f"Expected status 'ok', got {data}"
    except Exception as e:
        assert False, f"Failed to connect to Flask health endpoint: {e}"

def test_sanitizer_executable():
    """Verify that the sanitizer script exists and is executable."""
    path = "/home/user/sanitizer.py"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_sanitizer_adversarial_corpus():
    """Verify the sanitizer correctly classifies clean and evil inputs."""
    sanitizer_path = "/home/user/sanitizer.py"
    clean_corpus = "/home/user/corpora/clean.csv"
    evil_corpus = "/home/user/corpora/evil.csv"

    assert os.path.exists(clean_corpus), f"Clean corpus {clean_corpus} missing"
    assert os.path.exists(evil_corpus), f"Evil corpus {evil_corpus} missing"

    with open(clean_corpus, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    with open(evil_corpus, "r") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    clean_bypassed = []
    for line in clean_lines:
        res = subprocess.run(["python3", sanitizer_path, line], capture_output=True, text=True)
        if "SAFE" not in res.stdout:
            clean_bypassed.append(line)

    evil_bypassed = []
    for line in evil_lines:
        res = subprocess.run(["python3", sanitizer_path, line], capture_output=True, text=True)
        if "EVIL" not in res.stdout:
            evil_bypassed.append(line)

    errors = []
    if clean_bypassed:
        errors.append(f"{len(clean_bypassed)} of {len(clean_lines)} clean modified/rejected: {clean_bypassed[:5]}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_lines)} evil bypassed: {evil_bypassed[:5]}")

    assert not errors, " | ".join(errors)