# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_black_frame_count():
    """Check if the black frame count is correctly extracted and written."""
    path = "/home/user/black_frame_count.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "5", f"Expected black frame count to be '5', got '{content}'."

def test_sanitizer_executable():
    """Ensure the sanitizer C program is compiled and executable."""
    path = "/home/user/sanitizer"
    assert os.path.isfile(path), f"Sanitizer executable {path} does not exist."
    assert os.access(path, os.X_OK), f"Sanitizer {path} is not executable."

def test_adversarial_corpus():
    """
    Test the sanitizer against the adversarial corpus.
    Evil files must be rejected (exit code != 0).
    Clean files must be preserved (exit code == 0 and STDOUT matches file contents exactly).
    """
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        with open(filepath, "rb") as stdin_file:
            result = subprocess.run([sanitizer_path], stdin=stdin_file, capture_output=True)
            if result.returncode == 0:
                evil_bypassed.append(f)

    # Test clean corpus
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        with open(filepath, "rb") as stdin_file:
            expected_output = stdin_file.read()
            stdin_file.seek(0)
            result = subprocess.run([sanitizer_path], stdin=stdin_file, capture_output=True)
            if result.returncode != 0 or result.stdout != expected_output:
                clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_watchdog_exists():
    """Ensure the watchdog script is created and executable."""
    path = "/home/user/watchdog.sh"
    assert os.path.isfile(path), f"Watchdog script {path} does not exist."
    assert os.access(path, os.X_OK), f"Watchdog script {path} is not executable."

def test_nginx_endpoint():
    """Ensure Nginx is running and returning 200 OK for valid payloads."""
    payload = b'{"sensor":"temp","value":22.5}'
    req = urllib.request.Request("http://localhost:80/telemetry", data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx or received an error response: {e}")