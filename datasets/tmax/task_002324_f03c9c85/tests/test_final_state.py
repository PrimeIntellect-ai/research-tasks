# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error

def test_run_sanitizer_env_vars():
    script_path = "/home/user/run_sanitizer.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()

    assert "LANG=en_US.UTF-8" in content, "LANG=en_US.UTF-8 not exported in run_sanitizer.sh"
    assert "TZ=UTC" in content, "TZ=UTC not exported in run_sanitizer.sh"
    assert "BACKEND_PORT=9000" in content, "BACKEND_PORT=9000 not exported in run_sanitizer.sh"

def test_ssh_tunnel_active():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9000/ping", timeout=5)
        status = req.getcode()
        assert status == 200, f"Expected HTTP 200 OK from backend, got {status}"
    except urllib.error.URLError as e:
        assert False, f"Failed to reach backend via SSH tunnel on port 9000: {e}"
    except Exception as e:
        assert False, f"Unexpected error checking SSH tunnel: {e}"

def test_adversarial_corpus():
    sanitizer_bin = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_bin), f"Compiled binary {sanitizer_bin} not found."
    assert os.access(sanitizer_bin, os.X_OK), f"{sanitizer_bin} is not executable."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_rejected = []

    # Check evil corpus
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        result = subprocess.run([sanitizer_bin, filepath], capture_output=True, text=True)
        if result.returncode != 1 or "REJECTED" not in result.stdout:
            evil_bypassed.append(f)

    # Check clean corpus
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        result = subprocess.run([sanitizer_bin, filepath], capture_output=True, text=True)
        if result.returncode != 0 or "ACCEPTED" not in result.stdout:
            clean_rejected.append(f)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    assert not evil_bypassed and not clean_rejected, " | ".join(error_messages)