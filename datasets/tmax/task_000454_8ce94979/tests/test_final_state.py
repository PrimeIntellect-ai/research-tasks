# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_health():
    """Test that Nginx is correctly proxying to the new socket and returning 200 OK."""
    try:
        req = urllib.request.Request("http://localhost:8080/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 OK, got HTTPError {e.code}. Nginx proxying might still be broken.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx: {e.reason}. Is Nginx running?")

def test_nginx_config():
    """Verify that the Nginx configuration was updated with the correct socket and deny rule."""
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"Expected Nginx config {path} to exist."
    with open(path, "r") as f:
        content = f.read()

    assert "/tmp/cost_dashboard.sock" in content, "Expected nginx.conf to point to the correct upstream socket '/tmp/cost_dashboard.sock'."
    assert "198.51.100.55" in content and "deny" in content, "Expected nginx.conf to contain a deny directive for 198.51.100.55."

def test_run_filter_script_contents():
    """Check if the wrapper script sets the required environment variables."""
    script_path = "/home/user/run_filter.sh"
    assert os.path.isfile(script_path), f"Expected wrapper script {script_path} to exist."
    with open(script_path, "r") as f:
        content = f.read()

    assert "TZ=" in content and "Etc/UTC" in content, "run_filter.sh must set TZ to 'Etc/UTC'"
    assert "LC_ALL=" in content and "en_US.UTF-8" in content, "run_filter.sh must set LC_ALL to 'en_US.UTF-8'"
    assert "cost_filter.py" in content, "run_filter.sh must execute cost_filter.py"

def test_adversarial_corpus():
    """
    Test the admission controller against the clean and evil corpora.
    Clean corpus files must be accepted (exit code 0).
    Evil corpus files must be rejected (exit code 1).
    """
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    script_path = "/home/user/run_filter.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} to exist."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_modified = []
    evil_bypassed = []

    for f in clean_files:
        result = subprocess.run(["bash", script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    for f in evil_files:
        result = subprocess.run(["bash", script_path, f], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))