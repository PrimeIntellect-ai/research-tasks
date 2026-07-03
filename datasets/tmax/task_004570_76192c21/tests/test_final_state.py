# test_final_state.py
import os
import subprocess
import json
import urllib.request
import urllib.error
import pytest

def test_monitoring_stack_tunnel():
    """
    Validates that the full stack (SSH Tunnel -> Nginx -> Flask -> Redis) is properly configured
    and accessible via the local port 9000.
    """
    url = "http://127.0.0.1:9000/api/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
            assert data.get("redis") == "connected", f"Expected redis 'connected', got {data.get('redis')}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url} via SSH tunnel. Is the tunnel, Nginx, Flask, and Redis running? Error: {e}")
    except json.JSONDecodeError:
        pytest.fail("Failed to parse JSON response from API. The proxy or API might be misconfigured.")

def test_log_sanitization_script_executable():
    """
    Validates that the log sanitization script exists and is executable.
    """
    script_path = "/home/user/sanitize_logs.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable. Run chmod +x."

def test_log_sanitization_clean_corpus():
    """
    Validates that the sanitization script preserves 100% of the clean logs.
    """
    script_path = "/home/user/sanitize_logs.sh"
    clean_dir = "/home/user/corpus/clean_hidden"
    assert os.path.isdir(clean_dir), f"Clean corpus dir missing: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean corpus files found to test."

    modified_files = []
    for fpath in clean_files:
        with open(fpath, 'r') as f:
            expected_output = f.read()

        try:
            result = subprocess.run([script_path, fpath], capture_output=True, text=True, check=True)
            if result.stdout != expected_output:
                modified_files.append(os.path.basename(fpath))
        except subprocess.CalledProcessError:
            modified_files.append(os.path.basename(fpath) + " (script returned non-zero exit code)")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}")

def test_log_sanitization_evil_corpus():
    """
    Validates that the sanitization script drops 100% of the evil logs.
    """
    script_path = "/home/user/sanitize_logs.sh"
    evil_dir = "/home/user/corpus/evil_hidden"
    assert os.path.isdir(evil_dir), f"Evil corpus dir missing: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil corpus files found to test."

    bypassed_files = []
    for fpath in evil_files:
        try:
            result = subprocess.run([script_path, fpath], capture_output=True, text=True, check=True)
            # The output should be completely empty for evil lines
            if result.stdout.strip() != "":
                bypassed_files.append(os.path.basename(fpath))
        except subprocess.CalledProcessError:
            # Script failing on evil input is considered a failure to process cleanly, 
            # though depending on intent, failing might be acceptable. Assuming it should exit 0 and print nothing.
            bypassed_files.append(os.path.basename(fpath) + " (script returned non-zero exit code)")

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")